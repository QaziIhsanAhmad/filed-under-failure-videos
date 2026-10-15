"""Free API upload lane (lane "api"), added 15 Oct 2026. Replaces the 5 MB-limited Make download lane.

How it works (no paid tools, no secrets in this public repo):
  1. yt_feed.py (hourly) calls build_queue(): every lane=api row that is due within QUEUE_DAYS and not yet
     uploaded goes into yt/upload-queue.json with its YouTube metadata. Rows publish via YouTube's own
     scheduler: they are uploaded early as private with status.publishAt = their slot.
  2. Make scenario "FUF upload sessions" (daily) reads that queue, opens a resumable upload session per item
     through its already-authorised YouTube connection, and sends ONLY the session URL to GitHub
     (repository_dispatch "yt-session"). Make never downloads the file, so its 5 MB limit does not apply.
  3. yt-upload.yml / yt_upload.py streams the file from the repo into the session (any size) and writes
     yt/results/<id>.json. merge_results() (hourly) applies results to the ledger.
Episodes also get their thumbnail via the same route (kind "thumb") once the video id is known.
"""
import datetime as dt, glob, json, os

PKT = dt.timezone(dt.timedelta(hours=5))
QUEUE_DAYS = 8          # upload up to a week ahead; YouTube publishes at publishAt
MAX_ATTEMPTS = 3
VIDEO_PATH = "/../upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
THUMB_PATH = "/../upload/youtube/v3/thumbnails/set?uploadType=resumable&videoId={vid}"


def _clean(s, n):
    return (s or "").replace("<", "").replace(">", "")[:n]


def _tags(row):
    ep = row["id"].split("-")[0]
    for f in sorted(glob.glob(f"{ep}/{ep}-*.json")):
        try:
            tags = json.load(open(f)).get("tags") or []
        except Exception:
            continue
        out, total = [], 0
        for t in tags:
            if total + len(t) + 2 > 450:
                break
            out.append(t); total += len(t) + 2
        return out
    return []


def _slot(row):
    h, m = (row.get("time") or "21:00").split(":")
    return dt.datetime.combine(dt.date.fromisoformat(row["date"]), dt.time(int(h), int(m)), PKT)


def _file(row):
    for k in ("file_original", "file"):     # no size limit any more: prefer the full-quality original
        f = row.get(k, "")
        if f and not f.startswith("http") and os.path.exists(f):
            return f
    return ""


def _thumb(row):
    ep = row["id"].split("-")[0]
    hits = sorted(glob.glob(f"{ep}/{ep}-*thumbnail*.png"))
    return hits[0] if hits else ""


def merge_results(led, now):
    """Apply yt/results/*.json (written by yt_upload.py) to ledger rows. Idempotent."""
    by_id = {r["id"]: r for r in led["items"]}
    for f in sorted(glob.glob("yt/results/*.json")):
        res = json.load(open(f))
        row = by_id.get(res.get("row"))
        if not row or res.get("key") in row.setdefault("apiApplied", []):
            continue
        row["apiApplied"].append(res.get("key"))
        if res.get("kind") == "thumb":
            row["thumbSet"] = bool(res.get("ok"))
            if not res.get("ok"):
                row["thumbAttempts"] = row.get("thumbAttempts", 0) + 1
                row["thumbError"] = res.get("error")
            continue
        if res.get("ok") and res.get("videoId"):
            vid = res["videoId"]
            row.update(videoId=vid, url=f"https://www.youtube.com/{'shorts/' if row.get('type') == 'short' else 'watch?v='}{vid}",
                       status="published" if row.get("status") == "published" else "scheduled",
                       uploadedAt=res.get("at"), publishAt=res.get("publishAt"))
            row.pop("apiError", None)
        else:
            row["apiAttempts"] = row.get("apiAttempts", 0) + 1
            row["apiError"] = res.get("error")
            row["status"] = "paused-failed" if row["apiAttempts"] >= MAX_ATTEMPTS else "planned"


def build_queue(led, now, untitled):
    items = []
    for row in led["items"]:
        if row.get("lane") != "api":
            continue
        # thumbnail for an uploaded episode
        if row.get("videoId") and row.get("type") == "video" and not row.get("thumbSet") \
                and row.get("thumbAttempts", 0) < MAX_ATTEMPTS and _thumb(row):
            t = _thumb(row)
            items.append({"id": f"{row['id']}-thumb{row.get('thumbAttempts', 0)}", "row": row["id"], "kind": "thumb",
                          "file": t, "ctype": "image/png", "size": os.path.getsize(t), "meta": "{}",
                          "path": THUMB_PATH.format(vid=row["videoId"])})
            continue
        if row.get("status") not in ("planned", "retry") or row.get("videoId"):
            continue
        if untitled:          # never upload while an unexplained untitled video exists (could be a duplicate)
            continue
        slot = _slot(row)
        if slot > now + dt.timedelta(days=QUEUE_DAYS):
            continue
        f = _file(row)
        if not f:
            row["apiError"] = "file missing in repo"
            continue
        status = {"selfDeclaredMadeForKids": False,
                  "containsSyntheticMedia": bool((row.get("altered") or {}).get("disclose"))}
        if slot > now + dt.timedelta(minutes=30):
            status.update(privacyStatus="private", publishAt=slot.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        else:
            status["privacyStatus"] = "public"
        meta = {"snippet": {"title": _clean(row["title"], 100), "description": _clean(row.get("description", ""), 4900),
                            "tags": _tags(row), "categoryId": "27", "defaultLanguage": "en", "defaultAudioLanguage": "en"},
                "status": status}
        items.append({"id": f"{row['id']}-a{row.get('apiAttempts', 0)}", "row": row["id"], "kind": "video",
                      "file": f, "ctype": "video/mp4", "size": os.path.getsize(f),
                      "meta": json.dumps(meta, ensure_ascii=False), "path": VIDEO_PATH,
                      "publishAt": status.get("publishAt", "")})
    # One-off thumbnail replacements (yt/thumb-jobs.json): retried with a new id after a failure, max MAX_ATTEMPTS.
    try:
        jobs = json.load(open("yt/thumb-jobs.json"))
    except Exception:
        jobs = []
    for j in jobs:
        tries = sorted(glob.glob(f"yt/results/tj-{j['id']}-a*.json"))
        if any(json.load(open(t)).get("ok") for t in tries) or len(tries) >= MAX_ATTEMPTS or not os.path.exists(j["file"]):
            continue
        items.append({"id": f"tj-{j['id']}-a{len(tries)}", "row": None, "kind": "thumb", "file": j["file"],
                      "ctype": "image/png", "size": os.path.getsize(j["file"]), "meta": "{}",
                      "path": THUMB_PATH.format(vid=j["videoId"])})
    done = {os.path.basename(p)[:-5] for p in glob.glob("yt/results/*.json")}
    items = [i for i in items if i["id"] not in done]       # already attempted under this id
    json.dump({"generated": now.isoformat(), "items": items}, open("yt/upload-queue.json", "w"), indent=1, ensure_ascii=False)
    # Same items as a bare array: Make's JSON parser turns each element into its own bundle.
    json.dump([{k: i[k] for k in ("id", "path", "ctype", "size", "meta", "file")} for i in items],
              open("yt/upload-queue-items.json", "w"), indent=1, ensure_ascii=False)
    return items


def build_cleanup(led, now):
    """Videos on the channel that no record knows about and that are leftovers of the API lane (an opened
    upload session creates the video immediately; if the bytes never arrive it stays as an empty private
    placeholder). Only titles 'session test...' or duplicates of an api-lane row title qualify; anything in
    the ledger, published.json or yt/results is never deleted. Make deletes yt/delete-queue-items.json."""
    out = []
    try:
        ch = json.load(open("yt/channel-all.json"))
    except Exception:
        ch = {"videos": []}
    known = {r.get("videoId") for r in led["items"]} | {r.get("videoId") for r in led.get("history", [])}
    try:
        known |= {v["videoId"] for v in json.load(open("yt/published.json"))}
    except Exception:
        pass
    for f in glob.glob("yt/results/*.json"):
        known.add(json.load(open(f)).get("videoId"))
    api_titles = {_clean(r["title"], 100).strip() for r in led["items"] if r.get("lane") == "api"}
    for v in ch.get("videos", []):
        t = (v.get("title") or "").strip()
        if v["id"] in known:
            continue
        if t.startswith("session test") or t in api_titles:
            out.append({"id": v["id"], "title": t})
    json.dump(out, open("yt/delete-queue-items.json", "w"), indent=1, ensure_ascii=False)
    return out
