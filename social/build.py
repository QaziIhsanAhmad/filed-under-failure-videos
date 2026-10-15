"""Social posting lane for Xenova Solutions + FrontDesk Flows (free: GitHub + Make free plan).

social/posts/*.json   content batches (written by the weekly content routine; rendered by studio/render.js)
social/img/<brand>/   rendered slides <id>-<n>.jpg (1080x1350 JPEG, hosted via raw.githubusercontent.com)
social/results/       one file per platform callback from Make (record.py)
social/queue.json     merged view: every post with per-platform status (posted / failed / missed / planned)
social/due.json       bare array of TODAY's (PKT) unposted items; Make scenario "Social posts" reads it daily

Duplicate protection: an item is only ever "due" on its own date, and drops out as soon as Make reports any
attempt. A missed day is marked "missed", never posted late automatically (a person/routine can re-date it).
"""
import datetime as dt, glob, json, os, re

PKT = dt.timezone(dt.timedelta(hours=5))
RAW = "https://raw.githubusercontent.com/QaziIhsanAhmad/filed-under-failure-videos/main/social/img/"
BRANDS = {
    "xenova": {"fb_page": "1267773913096573", "ig_account": "17841428615145019", "li": True},
    "frontdesk": {"fb_page": "1354185007779555", "ig_account": "17841416945478586", "li": False},  # no FrontDesk LinkedIn page
}
POST_HOUR = 18   # Make runs 18:05 PKT = 14:05 BST / 13:05 GMT / 09:05 ET: UK afternoon + US East morning


def li_ltf(text):
    """LinkedIn 'little text format': escape reserved characters, keep hashtags clickable."""
    out = re.sub(r'([\\|{}@\[\]()<>*_~])', r'\\\1', text)
    return re.sub(r'#(\w+)', r'{hashtag|\\#|\1}', out)


def load_posts():
    posts = []
    for f in sorted(glob.glob("social/posts/*.json")):
        for p in json.load(open(f)):
            p["_src"] = f
            posts.append(p)
    return posts


def results():
    res = {}
    for f in sorted(glob.glob("social/results/*.json")):
        r = json.load(open(f))
        res.setdefault(r["id"], []).append(r)
    return res


MAX_TRIES = 3          # per platform
RETRY_DAYS = 3         # a failed platform is retried on the next daily runs, for up to 3 days after its date


def platform_state(p, res, brand):
    """Per platform: posted (the platform returned a post id = confirmed published), failed (attempted, no id),
    pending (never attempted). Only 'failed' platforms are ever retried; a posted platform is never sent again."""
    plats = ["fb", "ig"] + (["li"] if BRANDS[brand]["li"] and p["captions"].get("li") else [])
    out = {}
    for k in plats:
        tries = [x for x in res if k in x.get("platforms", "").split("+")]
        ids = [x.get(k) for x in tries if x.get(k)]
        out[k] = {"state": "posted" if ids else ("failed" if tries else "pending"), "id": ids[0] if ids else "",
                  "tries": len(tries), "at": tries[-1]["at"] if tries else ""}
    return out


def main():
    now = dt.datetime.now(PKT)
    today = now.date()
    res = results()
    queue, due, problems, seen = [], [], [], set()
    for p in load_posts():
        if p["id"] in seen:
            problems.append(f"duplicate id {p['id']}"); continue
        seen.add(p["id"])
        b = BRANDS[p["brand"]]
        n = len(p["slides"])
        imgs = [f"social/img/{p['brand']}/{p['id']}-{i + 1}.jpg" for i in range(n)]
        missing = [i for i in imgs if not os.path.exists(i)]
        plat = platform_state(p, res.get(p["id"], []), p["brand"])
        day = dt.date.fromisoformat(p["date"])
        states = {v["state"] for v in plat.values()}
        if states == {"posted"}:
            status = "posted"
        elif missing:
            status = "not-rendered"
        elif states == {"pending"}:
            status = "planned" if day > today or (day == today and now.hour < POST_HOUR + 2) else "missed"
        elif "pending" in states:
            status = "unverified"     # some platforms reported, others never did: check Make history, never auto-repost
        else:
            status = "partial" if "posted" in states else "failed"
        queue.append({"id": p["id"], "brand": p["brand"], "date": p["date"], "pillar": p.get("pillar", ""),
                      "slides": n, "status": status, "platforms": plat, "src": p["_src"]})
        if missing and day >= today:
            problems.append(f"{p['id']}: missing {', '.join(missing)}")
        if missing:
            continue
        if day == today:
            send = [k for k, v in plat.items() if v["state"] == "pending"]
        elif today - dt.timedelta(days=RETRY_DAYS) <= day < today:
            send = [k for k, v in plat.items() if v["state"] == "failed" and v["tries"] < MAX_TRIES]
        else:
            send = []
        if not send:
            continue
        urls = [RAW + i[len("social/img/"):] for i in imgs]
        c = p["captions"]
        due.append({"id": p["id"], "brand": p["brand"], "kind": "carousel" if n > 1 else "single",
                    "fb_on": "1" if "fb" in send else "0", "ig_on": "1" if "ig" in send else "0", "li_on": "1" if "li" in send else "0",
                    "fb_page": b["fb_page"], "ig_account": b["ig_account"],
                    "fb": c.get("fb") or c["ig"], "ig": c["ig"][:2200], "li": li_ltf(c.get("li", "")) if "li" in send else "",
                    "image": urls[0], "fb_photos": [{"type": "url", "url": u} for u in urls[:10]],
                    "ig_files": [{"media_type": "IMAGE", "image_url": u} for u in urls[:10]]})
    queue.sort(key=lambda q: (q["date"], q["brand"]))
    json.dump({"generated": now.isoformat(), "problems": problems, "items": queue}, open("social/queue.json", "w"), indent=1, ensure_ascii=False)
    json.dump(due, open("social/due.json", "w"), indent=1, ensure_ascii=False)
    print(f"{len(queue)} posts, {len(due)} due now, problems: {problems}")


if __name__ == "__main__":
    main()
