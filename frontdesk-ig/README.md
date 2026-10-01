# FrontDesk Flows Instagram queue

How posts reach @frontdeskflows:

1. A post is a JSON file in `queue/` (time, caption, image URL). Images live in `media/`.
2. Every hour, `.github/workflows/frontdesk-instagram.yml` runs `build_feed.py`, which writes `feed.xml` with every post whose `publish_after` time has passed.
3. Make.com (free plan) watches https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/frontdesk-ig/feed.xml and posts each new item to Instagram (photo URL = enclosure URL, caption = description).

Queue file format:

    {"publish_after": "2026-10-02T13:00:00+05:00",
     "caption": "Text with #hashtags",
     "media": [{"type": "image", "url": "https://raw.githubusercontent.com/.../media/xxx.jpg"}]}

Images: JPEG, 1080x1350 (4:5) or 1080x1080. Don't edit or rename a queue file after its time has passed, because Make may post it again.
