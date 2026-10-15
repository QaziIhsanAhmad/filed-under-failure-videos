"""Free YouTube publishing lane (no paid tools).

yt/ledger.json: one row per planned upload, lane metricool | make | native.
Only lane=make rows enter yt/feed.xml. Test clips live in yt/tests.json -> yt/test-feed.xml (never the production feed).

Row status flow (lane make):
  planned -> released (in feed) -> uploaded (Make reported videoId via repository_dispatch)
          -> published (seen on the public channel page or confirmed by Make callback + page)
  failed  (Make reported an error)            -> paused-failed
  no report from Make by 23:30 PKT on its day -> paused-unverified
  Paused items are NEVER re-released automatically. Only after a confirmed failure (Make History or
  YouTube Studio shows no video was created) is the status set to "retry"; the item is then released
  once under a NEW guid "<id>-rN" so Make's "already seen" memory cannot skip it.
Missing from the channel page alone = "unverified", never "failed".
"""
import datetime as dt, json, os, re, urllib.request, xml.etree.ElementTree as ET
from email.utils import format_datetime
from xml.sax.saxutils import escape

PKT = dt.timezone(dt.timedelta(hours=5))
CHANNEL = "UCI7G8N3yKI7pOyQU2glaJrQ"
HANDLE = "@FiledUnderFailure-d6j"
RELEASE_HOUR = 12      # enters the feed 12:00 PKT on its date (Make runs 21:00 PKT: 9 h margin)
RESULT_DEADLINE = dt.time(23, 30)
RAW = "https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/"
HDR = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30).read().decode("utf-8", "ignore")

def _add(out, vid, title, tab):
    if all(o["videoId"] != vid for o in out):
        out.append({"title": title, "videoId": vid, "tab": tab,
                    "url": f"https://www.youtube.com/{'watch?v=' if tab == 'videos' else 'shorts/'}{vid}"})

def _unescape(s):
    try:
        return json.loads('"' + s + '"')
    except Exception:          # a malformed snippet must never crash the whole run (it did from 10 Oct)
        return s.replace('\\u0026', '&').replace('\\"', '"')

def rss_feed(out, log):
    """Official channel RSS (latest ~15 uploads, videos and Shorts). Stable XML, no scraping."""
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    root = ET.fromstring(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"))
    n = 0
    for e in root.findall("a:entry", ns):
        vid = e.findtext("yt:videoId", "", ns); title = e.findtext("a:title", "", ns)
        link = (e.find("a:link", ns).get("href") if e.find("a:link", ns) is not None else "")
        if vid:
            _add(out, vid, title, "shorts" if "/shorts/" in link else "videos"); n += 1
    log.append(f"rss: {n}")

def channel_page():
    """Videos visible publicly (RSS first, then channel tabs). None = nothing could be read."""
    out, log, ok = [], [], False
    try:
        rss_feed(out, log); ok = True
    except Exception as e:
        log.append(f"rss: {type(e).__name__}: {e}")
    for tab in ("videos", "shorts"):
        try:
            html = get(f"https://www.youtube.com/{HANDLE}/{tab}"); ok = True
            if tab == "videos":
                pairs = re.findall(r'"videoRenderer":\{"videoId":"([\w-]{11})".*?"title":\{"runs":\[\{"text":"(.*?)"\}', html)
                pairs += re.findall(r'"contentId":"([\w-]{11})".{0,3000}?"title":\{"content":"(.*?)"', html)
            else:
                pairs = [(v, t) for t, v in re.findall(r'"accessibilityText":"(.*?), [\d.,KM]+ views?[^"]*".{0,1500}?"videoId":"([\w-]{11})"', html)]
            for vid, title in pairs:
                _add(out, vid, _unescape(title), tab)
            log.append(f"{tab}: {len(pairs)}")
        except Exception as e:
            log.append(f"{tab}: {type(e).__name__}: {e}")
    return (out if ok else None), log

def guid(it):
    return it["id"] + (f"-r{it['retries']}" if it.get("retries") else "")

def write_feed(path, title, items, now):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>',
           f"<title>{escape(title)}</title>", f"<link>https://www.youtube.com/{HANDLE}</link>",
           "<description>Filed Under Failure uploads</description>"]
    for it in items:
        url = it["file"] if it["file"].startswith("http") else RAW + it["file"]
        out += ["<item>", f"<title>{escape(it['title'])}</title>",
                f'<guid isPermaLink="false">{escape(guid(it))}</guid>',
                f"<link>{escape(url)}</link>", f"<pubDate>{format_datetime(it.get('_rel', now))}</pubDate>",
                f"<description>{escape(it['description'])}</description>",
                f'<enclosure url="{escape(url)}" type="video/mp4" length="0"/>', "</item>"]
    out.append("</channel></rss>")
    open(path, "w").write("\n".join(out) + "\n")

def main():
    now = dt.datetime.now(PKT)
    led = json.load(open("yt/ledger.json"))
    runs = json.load(open("yt/runs.json")) if os.path.exists("yt/runs.json") else {}
    ev = os.environ.get("GITHUB_EVENT_NAME", "local")
    runs["last_" + ev] = now.isoformat()
    json.dump(runs, open("yt/runs.json", "w"), indent=1)

    live, log = channel_page()
    open("yt/check.log", "w").write(now.isoformat() + "\n" + "\n".join(log) + "\n")
    by_title = {}
    if live is not None:
        json.dump(live, open("yt/published.json", "w"), indent=1, ensure_ascii=False)
        by_title = {v["title"].strip().lower(): v for v in live}
    # Videos YouTube created without metadata (title "unknown"); unknown channel state counts too.
    untitled = [v["videoId"] for v in live if v["title"].strip().lower() in ("unknown", "")] if live is not None else ["channel unreadable"]

    for it in led["items"]:
        seen = by_title.get(it["title"].strip().lower())
        if seen and it.get("status") != "published":
            it.update(status="published", url=seen["url"], videoId=seen["videoId"], verifiedAt=now.isoformat(), verification="channel page")
            continue
        if it["lane"] != "make" or it.get("status") in ("published", "uploaded") or str(it.get("status","")).startswith("paused"):
            continue
        day = dt.date.fromisoformat(it["date"])
        due = dt.datetime.combine(day, RESULT_DEADLINE, PKT)
        if it.get("releasedAt"):
            # Catch-up items released late must get a Make run first: wait until 23:30 PKT of the day of
            # the first 21:00 Make run at/after release (before this, late items were paused unseen).
            rel_at = dt.datetime.fromisoformat(it["releasedAt"]).astimezone(PKT)
            make_day = rel_at.date() if rel_at.time() < dt.time(20, 45) else rel_at.date() + dt.timedelta(days=1)
            due = max(due, dt.datetime.combine(make_day, RESULT_DEADLINE, PKT))
        if it.get("status") == "released" and now > due:
            # No report from Make. The upload may still be processing, private/unlisted, or simply
            # missing from the public page, so this is NOT a failure: pause and wait for review.
            it["status"] = "paused-unverified"
            it["note"] = "no result from Make by 23:30 PKT; check Make History / YouTube Studio before any retry"
        elif it.get("status") == "failed" and untitled:
            # 14 Oct: Make reported 3 upload errors but YouTube still created 3 videos titled
            # "unknown". While any such video exists, a retry could duplicate one: hold instead.
            it["status"] = "paused-unknown-video"
            it["note"] = "Make error, but untitled video(s) exist on the channel: " + ", ".join(untitled) + " - fix titles, do not re-upload"
        elif it.get("status") == "failed" and it.get("retries", 0) < 2 and not it.get("videoId") \
                and any(r.get("event") == "yt-failed" for r in it.get("results", [])[-1:]):
            # Make reported an error and returned no videoId: YouTube created no video, so a retry
            # cannot duplicate. Auto-retry (max 2) on the next 21:00 run instead of waiting for a
            # human or a monitor run (those kept dying on usage limits, leaving uploads stuck).
            it["retries"] = it.get("retries", 0) + 1
            it["status"] = "planned"
            it["date"] = (now.date() if now.hour < 20 else now.date() + dt.timedelta(days=1)).isoformat()
            it["note"] = f"auto-retry {it['retries']} after Make error at {now.isoformat()}"
        elif it.get("status") == "failed":
            it["status"] = "paused-failed"
            it["note"] = "Make reported an error; confirm in YouTube Studio that no video was created, then set status 'retry'"
        elif it.get("status") == "retry":
            # Set only by a person or the monitor AFTER confirming (Make History / YouTube Studio) that
            # no video exists. Re-released once under a new guid so Make treats it as new.
            it["retries"] = it.get("retries", 0) + 1
            it["status"] = "planned"
            it["date"] = (now.date() if now.hour < 20 else now.date() + dt.timedelta(days=1)).isoformat()

    feed = []
    for it in led["items"]:
        if it["lane"] != "make" or it.get("status") not in ("planned", "released"):
            continue
        day = dt.date.fromisoformat(it["date"])
        rel = dt.datetime.combine(day, dt.time(RELEASE_HOUR), PKT)
        if now >= rel:                          # catch-up: stays in the feed until a result arrives
            if it.get("status") == "planned":       # fresh release (incl. retries): new timestamp
                it["releasedAt"] = now.isoformat()
            it["status"] = "released"; it["_rel"] = rel
            feed.append(it)
    # Free API lane (see yt/yt_api.py): apply upload results, then rebuild the upload queue for Make.
    import sys; sys.path.insert(0, "yt")
    import yt_api
    yt_api.merge_results(led, now)
    yt_api.build_queue(led, now, [u for u in untitled if u != "channel unreadable"])
    write_feed("yt/feed.xml", "Filed Under Failure uploads", feed, now)
    for it in led["items"]:
        it.pop("_rel", None)
    json.dump(led, open("yt/ledger.json", "w"), indent=1, ensure_ascii=False)

    tests = json.load(open("yt/tests.json"))
    write_feed("yt/test-feed.xml", "Filed Under Failure TEST uploads", [t for t in tests["items"] if t.get("status") != "deleted"], now)

if __name__ == "__main__":
    main()
