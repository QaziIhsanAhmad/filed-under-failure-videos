"""Record stats sent by Make (repository_dispatch yt-stats / yt-analytics) into yt/stats/<type>-<date>.json.
yt-stats payload: {ids, views, likes, comments} comma lists (YouTube Data API, public counters).
yt-analytics payload: {status, cols, rows} rows = flattened YouTube Analytics report (dimension=video)."""
import datetime as dt, json, os
ev = json.load(open(os.environ["GITHUB_EVENT_PATH"]))
kind, p = ev["action"], ev.get("client_payload", {})
now = dt.datetime.now(dt.timezone(dt.timedelta(hours=5)))
os.makedirs("yt/stats", exist_ok=True)
out = {"at": now.isoformat(), "kind": kind}
if kind == "yt-stats":
    sp = lambda k: (p.get(k) or "").split(",")
    out["videos"] = [{"id": i, "views": int(v or 0), "likes": int(l or 0), "comments": int(c or 0)}
                     for i, v, l, c in zip(sp("ids"), sp("views"), sp("likes"), sp("comments")) if i]
else:
    cols = [c for c in (p.get("cols") or "").split(",") if c]
    flat = (p.get("rows") or "").split(",") if p.get("rows") else []
    out.update(status=p.get("status"), error=p.get("error"), cols=cols,
               rows=[flat[n:n + len(cols)] for n in range(0, len(flat), len(cols))] if cols else [])
json.dump(out, open(f"yt/stats/{kind}-{now.date()}.json", "w"), indent=1, ensure_ascii=False)
print(kind, "recorded")
