"""Build xenova/social-feed.xml from social-queue.json: items whose date has reached 12:00 PKT and are not posted."""
import json, datetime as dt
from email.utils import format_datetime
from xml.sax.saxutils import escape
PKT = dt.timezone(dt.timedelta(hours=5))
now = dt.datetime.now(PKT)
q = json.load(open("xenova/social-queue.json"))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>', "<title>Xenova social</title>",
       "<link>https://xenovasolutions.com</link>", "<description>Xenova FB+IG queue</description>"]
for i in sorted(q["items"], key=lambda i: i["date"]):
    rel = dt.datetime.fromisoformat(i["release"]) if i.get("release") else dt.datetime.combine(dt.date.fromisoformat(i["date"]), dt.time(12), PKT)
    if i["status"] != "planned" or now < rel:
        continue
    out += ["<item>", f"<title>{escape(i['id'])}</title>", f'<guid isPermaLink="false">{escape(i["id"])}</guid>',
            f"<link>{escape(i['image'])}</link>", f"<pubDate>{format_datetime(rel)}</pubDate>",
            f"<description>{escape(i['caption'])}</description>", "</item>"]
out.append("</channel></rss>")
open("xenova/social-feed.xml", "w").write("\n".join(out) + "\n")
