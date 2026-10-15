"""Generic YouTube Data API operations through the Make YouTube connection (free; no secrets in this repo).

yt/ops.json        list of ops: {id, method, path, body?, after?: [op ids]}; body may contain placeholders:
                   "@res:<op>"  -> resource id returned by that op (e.g. a new playlist id)
                   "@desc:<op>" -> the description that op fetched (GET /v3/videos?part=snippet&id=...)
                   Ops with transform {"kind": "prepend"|"append"|"replace_line", ...} edit a fetched description.
yt/ops-queue-items.json  ops ready to run now (deps done), max BATCH; Make runs them and reports back.
yt/ops-done/<id>.json    result per op {id, code, res, desc?}; failed ops retry up to MAX_TRIES.
Uses: playlists, playlist items, retitles/description fixes, Shorts -> full-episode links.
"""
import base64, glob, json, os

BATCH = 15
MAX_GETS = 6          # GET results carry the whole description (base64): keep the GitHub dispatch payload small
MAX_TRIES = 2


def done():
    out = {}
    for f in glob.glob("yt/ops-done/*.json"):
        r = json.load(open(f))
        out.setdefault(r["id"], []).append(r)
    return out


def ok(rs):
    return any(str(r.get("code", "")).startswith("2") for r in rs)


def _desc(rs):
    for r in rs:
        if r.get("desc"):
            try:
                return base64.b64decode(r["desc"]).decode("utf-8")
            except Exception:
                return None
    return None


def resolve(op, d):
    body = op.get("body")
    if body is None:
        return ""
    s = json.dumps(body, ensure_ascii=False)
    for dep in op.get("after", []):
        rs = d.get(dep, [])
        res = next((r.get("res") for r in rs if r.get("res")), "")
        s = s.replace(f"@res:{dep}", res)
        if f"@desc:{dep}" in s:
            desc = _desc(rs)
            if desc is None:
                return None
            t = op.get("transform") or {}
            if t.get("kind") == "prepend" and t["text"].split("\n")[0] not in desc:
                desc = t["text"] + "\n\n" + desc
            elif t.get("kind") == "replace_line":
                lines = [l for l in desc.split("\n") if not l.startswith(t["prefix"])]
                desc = t["text"] + "\n\n" + "\n".join(lines).lstrip("\n")
            if t.get("append") and t["append"].split("\n")[0] not in desc:
                desc = desc.rstrip() + "\n\n" + t["append"]
            s = s.replace(f'"@desc:{dep}"', json.dumps(desc[:4900], ensure_ascii=False))
    return s


def build():
    ops = json.load(open("yt/ops.json")) if os.path.exists("yt/ops.json") else []
    d = done()
    items, status = [], {}
    for op in ops:
        rs = d.get(op["id"], [])
        if ok(rs):
            status[op["id"]] = "done"; continue
        if len(rs) >= MAX_TRIES:
            status[op["id"]] = "failed: " + str(rs[-1].get("code")); continue
        if not all(ok(d.get(a, [])) for a in op.get("after", [])):
            status[op["id"]] = "waiting"; continue
        body = resolve(op, d)
        if body is None:
            status[op["id"]] = "waiting (no description fetched)"; continue
        status[op["id"]] = "queued"
        if len(items) < BATCH and (op["method"] != "GET" or sum(i["method"] == "GET" for i in items) < MAX_GETS):
            items.append({"id": op["id"], "method": op["method"], "path": op["path"], "body": "" if op["method"] == "GET" else (body or "{}")})
    json.dump(items, open("yt/ops-queue-items.json", "w"), indent=1, ensure_ascii=False)
    json.dump(status, open("yt/ops-status.json", "w"), indent=1)
    return items


def record(rows, at):
    """rows: 'id|code|res|b64desc' joined by ';;' (Make text aggregator)."""
    os.makedirs("yt/ops-done", exist_ok=True)
    for row in [r for r in rows.split(";;") if r.strip()]:
        parts = (row.split("|") + ["", "", "", ""])[:4]
        oid = "".join(c for c in parts[0] if c.isalnum() or c in "-_")
        if not oid:
            continue
        n = len(glob.glob(f"yt/ops-done/{oid}*.json"))
        json.dump({"id": oid, "code": parts[1].strip(), "res": parts[2].strip(), "desc": parts[3].strip(), "at": at},
                  open(f"yt/ops-done/{oid}.{n}.json", "w"), indent=1)


if __name__ == "__main__":
    import datetime as dt, sys
    if len(sys.argv) > 1 and sys.argv[1] == "record":
        ev = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["client_payload"]
        record(ev.get("rows", ""), dt.datetime.now(dt.timezone.utc).isoformat())
    print(len(build()), "ops queued")
