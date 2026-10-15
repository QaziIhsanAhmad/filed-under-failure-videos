"""repository_dispatch 'social-posted' from Make -> social/results/<id>-<platforms>.json.
Payload: {id, platforms: "fb+ig" | "li", fb, ig, li} (empty id = that platform failed)."""
import datetime as dt, json, os, re

ev = json.load(open(os.environ["GITHUB_EVENT_PATH"]))["client_payload"]
pid = re.sub(r"[^\w-]", "", ev.get("id", ""))[:80]
plats = re.sub(r"[^a-z+]", "", ev.get("platforms", ""))[:12]
if pid:
    os.makedirs("social/results", exist_ok=True)
    rec = {"id": pid, "platforms": plats, "at": dt.datetime.now(dt.timezone.utc).isoformat()}
    for k in ("fb", "ig", "li"):
        if k in plats:
            rec[k] = str(ev.get(k, ""))[:120]
    stamp = rec["at"][:19].replace(":", "").replace("-", "")
    json.dump(rec, open(f"social/results/{pid}-{plats.replace('+', '')}-{stamp}.json", "w"), indent=1)   # one file per attempt
    print(rec)
