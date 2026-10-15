"""Stream one queued file into a YouTube resumable upload session opened by Make (see yt/yt_api.py).
Input: repository_dispatch "yt-session" with client_payload {id, session}. The session URL is a single-use
capability; it is read from the event file only and never printed. Output: yt/results/<id>.json."""
import datetime as dt, json, os, sys, urllib.error, urllib.request

PKT = dt.timezone(dt.timedelta(hours=5))
ev = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
p = ev.get("client_payload", {})
qid, session = (p.get("id") or "").strip(), (p.get("session") or "").strip()
os.makedirs("yt/results", exist_ok=True)
out = f"yt/results/{qid}.json"
now = dt.datetime.now(PKT).isoformat()

item = next((i for i in json.load(open("yt/upload-queue.json"))["items"] if i["id"] == qid), None)
res = {"key": qid, "row": item["row"] if item else None, "kind": item["kind"] if item else None, "at": now, "ok": False}

def finish(**kw):
    res.update(kw)
    json.dump(res, open(out, "w"), indent=1)
    print(qid, "ok" if res["ok"] else "FAILED", res.get("videoId", ""), res.get("error", ""))
    sys.exit(0)

if os.path.exists(out) and json.load(open(out)).get("ok"):
    print(qid, "already done"); sys.exit(0)
if not item:
    finish(error="id not in upload-queue.json")
if not session.startswith("https://www.googleapis.com/upload/youtube/v3/"):
    finish(error="missing or invalid session URL (Make could not open a session)")

size = os.path.getsize(item["file"])
req = urllib.request.Request(session, data=open(item["file"], "rb"), method="PUT",
                             headers={"Content-Type": item["ctype"], "Content-Length": str(size)})
try:
    with urllib.request.urlopen(req, timeout=1800) as r:
        body = json.loads(r.read().decode() or "{}")
except urllib.error.HTTPError as e:
    finish(error=f"HTTP {e.code}: {e.read().decode(errors='ignore')[:300]}")
except Exception as e:
    finish(error=f"{type(e).__name__}: {e}"[:300])

if item["kind"] == "thumb":
    finish(ok=True)
vid = body.get("id")
st = body.get("status", {})
finish(ok=bool(vid), videoId=vid, uploadStatus=st.get("uploadStatus"), privacy=st.get("privacyStatus"),
       publishAt=st.get("publishAt") or item.get("publishAt"), error=None if vid else f"no video id: {str(body)[:200]}")
