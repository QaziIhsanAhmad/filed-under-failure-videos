"""Publish the next due post in frontdesk-ig/queue/ to Instagram (@frontdeskflows).

Queue file (frontdesk-ig/queue/<YYYY-MM-DD-HHMM>-<slug>.json):
  {"publish_after": "2026-10-03T13:00:00+05:00",   # ISO time, post on/after this
   "caption": "text with #hashtags",
   "media": [{"type": "image", "url": "https://...jpg"}]}
  - 1 image  -> single photo post
  - 2-10 images/videos -> carousel
  - 1 {"type": "video", "url": ".../reel.mp4"} -> Reel
Media URLs must be public (raw.githubusercontent.com works). Images must be JPEG.

Env: IG_ACCESS_TOKEN, IG_USER_ID. Publishes at most one post per run, then moves
the file to posted/ with the media id. Exits non-zero on any API error.
"""
import json, os, sys, time, glob, shutil, datetime as dt
import urllib.request, urllib.parse, urllib.error

API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ["IG_ACCESS_TOKEN"]
USER = os.environ["IG_USER_ID"]
HERE = os.path.dirname(os.path.abspath(__file__))


def call(method, path, **params):
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{path}"
    req = urllib.request.Request(url, data=data, method="POST") if method == "POST" \
        else urllib.request.Request(f"{url}?{data.decode()}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Instagram API error on {path}: {e.code} {e.read().decode()[:500]}")


def wait_ready(cid):
    for _ in range(60):  # up to ~10 min for videos
        st = call("GET", cid, fields="status_code").get("status_code")
        if st == "FINISHED":
            return
        if st in ("ERROR", "EXPIRED"):
            sys.exit(f"Container {cid} failed: {st}")
        time.sleep(10)
    sys.exit(f"Container {cid} not ready in time")


def container(m, carousel_item=False, caption=None):
    p = {}
    if m["type"] == "video":
        p.update(media_type="VIDEO" if carousel_item else "REELS", video_url=m["url"])
    else:
        p["image_url"] = m["url"]
    if carousel_item:
        p["is_carousel_item"] = "true"
    if caption is not None:
        p["caption"] = caption
    cid = call("POST", f"{USER}/media", **p)["id"]
    wait_ready(cid)
    return cid


def main():
    now = dt.datetime.now(dt.timezone.utc)
    due = []
    for f in sorted(glob.glob(os.path.join(HERE, "queue", "*.json"))):
        post = json.load(open(f))
        when = dt.datetime.fromisoformat(post["publish_after"])
        if when <= now:
            due.append((when, f, post))
    if not due:
        print("Nothing due.")
        return
    _, f, post = sorted(due)[0]
    media = post["media"]
    if not 1 <= len(media) <= 10:
        sys.exit(f"{f}: media must have 1-10 items")
    if len(media) == 1:
        cid = container(media[0], caption=post["caption"])
    else:
        kids = [container(m, carousel_item=True) for m in media]
        cid = call("POST", f"{USER}/media", media_type="CAROUSEL",
                   children=",".join(kids), caption=post["caption"])["id"]
        wait_ready(cid)
    media_id = call("POST", f"{USER}/media_publish", creation_id=cid)["id"]
    link = call("GET", media_id, fields="permalink").get("permalink", "")
    post.update(published_at=now.isoformat(), media_id=media_id, permalink=link)
    dest = os.path.join(HERE, "posted", os.path.basename(f))
    json.dump(post, open(dest, "w"), indent=2)
    os.remove(f)
    print(f"Published {os.path.basename(f)} -> {link}")


if __name__ == "__main__":
    main()
