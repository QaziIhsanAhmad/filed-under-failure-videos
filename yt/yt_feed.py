"""Free YouTube publishing lane (no paid tools).

yt/ledger.json: one row per planned upload, lane metricool | make | native.
Only lane=make rows enter yt/feed.xml. Test clips live in yt/tests.json -> yt/test-feed.xml (never the production feed).

Row status flow (lane make):
  planned -> released (in feed) -> uploaded (Make reported videoId via repository_dispatch)
          -> published (seen on the public channel page or confirmed by Make callback + page)
  failed  (Make reported an error) or noresult (no report by 23:30 PKT on its day)
          -> reconcile: if the title is on the channel page, record it (no retry);
             otherwise after a second check re-release under a NEW guid "<id>-rN" (max 2 retries),
             so Make's "already seen" memory can never silently swallow a failed upload.
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
MAX_RETRIES = 2
RAW = "https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/"
HDR = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=30).read().decode("utf-8", "ignore")

def channel_page():
    """Videos visible on the public channel tabs. None = page could not be read."""
    out, log, ok = [], [], False
    for tab in ("videos", "shorts"):
        try:
            html = get(f"https://www.youtube.com/{HANDLE}/{tab}"); ok = True
        except Exception as e:
            log.append(f"{tab}: {e}"); continue
        if tab == "videos":
            pairs = re.findall(r'"videoRenderer":\{"videoId":"([\w-]{11})".*?"title":\{"runs":\[\{"text":"(.*?)"\}', html)
            pairs += re.findall(r'"contentId":"([\w-]{11})".{0,3000}?"title":\{"content":"(.*?)"', html)
        else:
            pairs = [(v, t) for t, v in re.findall(r'"accessibilityText":"(.*?), [\d.,KM]+ views?[^"]*".{0,1500}?"videoId":"([\w-]{11})"', html)]
        for vid, title in pairs:
            title = json.loads('"' + title + '"')
            if all(o["videoId"] != vid for o in out):
                out.append({"title": title, "videoId": vid, "tab": tab,
                            "url": f"https://www.youtube.com/{'watch?v=' if tab == 'videos' else 'shorts/'}{vid}"})
        log.append(f"{tab}: {len(pairs)}")
    return (out if ok else None), log

def guid(it):
    return it["id"] + (f"-r{it['retries']}" if it.get("retries") else "")

def write_feed(path, title, items, now):
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>',
           f"<title>{escape(title)}</title>", f"<link>https://www.youtube.com/{HANDLE}</link>",
           "<description>Filed Under Failure uploads</description>"]
    for it in items:
        url = RAW + it["file"]
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

    for it in led["items"]:
        seen = by_title.get(it["title"].strip().lower())
        if seen and it.get("status") != "published":
            it.update(status="published", url=seen["url"], videoId=seen["videoId"], verifiedAt=now.isoformat(), verification="channel page")
            continue
        if it["lane"] != "make" or it.get("status") in ("published", "uploaded", "gaveup"):
            continue
        day = dt.date.fromisoformat(it["date"])
        due = dt.datetime.combine(day, RESULT_DEADLINE, PKT)
        if it.get("status") == "released" and now > due:
            it["status"] = "noresult"
        if it.get("status") in ("failed", "noresult"):
            if live is None:
                continue                      # cannot reconcile without the channel page
            checks = it.get("reconcileChecks", 0) + 1
            it["reconcileChecks"] = checks
            if checks >= 2:                    # two hourly checks, still not on the channel page
                if it.get("retries", 0) >= MAX_RETRIES:
                    it["status"] = "gaveup"; it["note"] = "needs Qazi: check Make History and YouTube Studio"
                else:
                    it["retries"] = it.get("retries", 0) + 1
                    it["status"] = "planned"; it["reconcileChecks"] = 0
                    it["date"] = (now.date() if now.hour < 20 else now.date() + dt.timedelta(days=1)).isoformat()

    feed = []
    for it in led["items"]:
        if it["lane"] != "make" or it.get("status") not in ("planned", "released"):
            continue
        day = dt.date.fromisoformat(it["date"])
        rel = dt.datetime.combine(day, dt.time(RELEASE_HOUR), PKT)
        if now >= rel:                          # catch-up: stays in the feed until a result arrives
            it["status"] = "released"; it.setdefault("releasedAt", now.isoformat()); it["_rel"] = rel
            feed.append(it)
    write_feed("yt/feed.xml", "Filed Under Failure uploads", feed, now)
    for it in led["items"]:
        it.pop("_rel", None)
    json.dump(led, open("yt/ledger.json", "w"), indent=1, ensure_ascii=False)

    tests = json.load(open("yt/tests.json"))
    write_feed("yt/test-feed.xml", "Filed Under Failure TEST uploads", [t for t in tests["items"] if t.get("status") != "deleted"], now)

if __name__ == "__main__":
    main()
