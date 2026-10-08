"""Free YouTube publishing lane (no paid tools).

yt/ledger.json lists every planned upload once, with its lane:
  metricool  already scheduled in Metricool (never put in the feed: prevents duplicates)
  make       released into yt/feed.xml on its day; Qazi's Make.com scenario uploads it
  native     uploaded/scheduled by hand in YouTube Studio (kit in yt/native/)
Each run also reads the public channel feed and records what is actually live
(yt/published.json) so publication is verified, not assumed.
"""
import datetime as dt, json, os, urllib.request, xml.etree.ElementTree as ET
from email.utils import format_datetime
from xml.sax.saxutils import escape

PKT = dt.timezone(dt.timedelta(hours=5))
CHANNEL = "UCI7G8N3yKI7pOyQU2glaJrQ"
RELEASE_HOUR = 12  # item enters the feed at 12:00 PKT on its day; Make runs at 18:00 PKT
RAW = "https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/"

def published():
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL}"
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en"})
        root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    except Exception as e:  # keep previous record if YouTube is unreachable
        open("yt/check.log", "w").write(f"{dt.datetime.now(PKT).isoformat()} channel feed error: {e}\n")
        print("channel feed error:", e); return None
    open("yt/check.log", "w").write(f"{dt.datetime.now(PKT).isoformat()} channel feed ok\n")
    out = []
    for en in root.findall("a:entry", ns):
        vid = en.find("yt:videoId", ns).text
        out.append({"title": en.find("a:title", ns).text, "videoId": vid,
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "published": en.find("a:published", ns).text})
    return out

def main():
    now = dt.datetime.now(PKT)
    led = json.load(open("yt/ledger.json"))
    pub = published()
    if pub is not None:
        json.dump(pub, open("yt/published.json", "w"), indent=1, ensure_ascii=False)
        live = {p["title"].strip().lower(): p for p in pub}
        for it in led["items"]:
            p = live.get(it["title"].strip().lower())
            if p and it.get("status") != "published":
                it.update(status="published", url=p["url"], publishedAt=p["published"])
    feed = []
    for it in led["items"]:
        if it["lane"] != "make" or it.get("status") == "published":
            continue
        day = dt.date.fromisoformat(it["date"])
        release = dt.datetime.combine(day, dt.time(RELEASE_HOUR), PKT)
        if now >= release and now.date() - day <= dt.timedelta(days=2):
            feed.append((release, it))
            it.setdefault("status", "released")
            if it["status"] == "planned": it["status"] = "released"
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>',
           "<title>Filed Under Failure uploads</title>",
           "<link>https://www.youtube.com/channel/" + CHANNEL + "</link>",
           "<description>Videos due today</description>"]
    for release, it in sorted(feed, key=lambda x: x[0]):
        url = RAW + it["file"]
        out += ["<item>", f"<title>{escape(it['title'])}</title>",
                f'<guid isPermaLink="false">{escape(it["id"])}</guid>',
                f"<link>{escape(url)}</link>", f"<pubDate>{format_datetime(release)}</pubDate>",
                f"<description>{escape(it['description'])}</description>",
                f'<enclosure url="{escape(url)}" type="video/mp4" length="0"/>', "</item>"]
    out.append("</channel></rss>")
    open("yt/feed.xml", "w").write("\n".join(out) + "\n")
    json.dump(led, open("yt/ledger.json", "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    main()
