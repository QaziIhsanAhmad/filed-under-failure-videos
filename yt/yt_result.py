"""Records Make's upload result (repository_dispatch yt-uploaded / yt-failed) against the ledger row or test."""
import datetime as dt, json, os
PKT = dt.timezone(dt.timedelta(hours=5))
ev = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
kind, p = ev["action"], ev.get("client_payload", {})
g = (p.get("guid") or "").strip()
now = dt.datetime.now(PKT).isoformat()
path = "yt/tests.json" if g.startswith("test-") else "yt/ledger.json"
doc = json.load(open(path))
base = g.split("-r")[0] if "-r" in g and g.rsplit("-r", 1)[1].isdigit() else g
for it in doc["items"]:
    if it["id"] == base:
        rec = {"at": now, "event": kind, "guid": g, "videoId": p.get("videoId"), "uploadStatus": p.get("uploadStatus"),
               "privacy": p.get("privacy"), "error": p.get("error")}
        it.setdefault("results", []).append(rec)
        if kind == "yt-uploaded" and p.get("videoId"):
            it.update(status="uploaded", videoId=p["videoId"], url=f"https://www.youtube.com/watch?v={p['videoId']}")
        elif kind == "yt-failed" and it.get("status") != "uploaded":
            it["status"] = "failed"
        break
else:
    doc.setdefault("unmatched", []).append({"at": now, "event": kind, "payload": p})
json.dump(doc, open(path, "w"), indent=1, ensure_ascii=False)
print(kind, g, path)
