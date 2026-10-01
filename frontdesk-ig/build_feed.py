"""Build frontdesk-ig/feed.xml: an RSS feed of queued posts whose publish_after time has passed.

Make.com watches this feed (RSS > Watch RSS feed items) and posts each new item to
@frontdeskflows (Instagram for Business > Create a Photo Post):
  photo URL = the item's enclosure URL, caption = the item's description.
Items stay in the feed; Make only posts items it hasn't seen (guid = queue file name).
"""
import glob, json, os, datetime as dt
from email.utils import format_datetime
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
now = dt.datetime.now(dt.timezone.utc)
items = []
for f in glob.glob(os.path.join(HERE, "queue", "*.json")):
    p = json.load(open(f))
    when = dt.datetime.fromisoformat(p["publish_after"])
    if when <= now and p["media"] and p["media"][0]["type"] == "image":
        items.append((when, os.path.splitext(os.path.basename(f))[0], p))
items.sort(reverse=True)

out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>',
       "<title>FrontDesk Flows Instagram queue</title>",
       "<link>https://www.instagram.com/frontdeskflows/</link>",
       "<description>Posts due for @frontdeskflows</description>"]
for when, gid, p in items[:20]:
    url = p["media"][0]["url"]
    out += ["<item>", f"<title>{escape(gid)}</title>", f'<guid isPermaLink="false">{escape(gid)}</guid>',
            f"<link>{escape(url)}</link>", f"<pubDate>{format_datetime(when)}</pubDate>",
            f"<description>{escape(p['caption'])}</description>",
            f'<enclosure url="{escape(url)}" type="image/jpeg" length="0"/>', "</item>"]
out.append("</channel></rss>")
open(os.path.join(HERE, "feed.xml"), "w").write("\n".join(out) + "\n")
print(f"feed.xml: {len(items[:20])} item(s)")
