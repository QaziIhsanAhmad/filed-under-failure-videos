"""Record the channel's own video list (incl. private/scheduled) sent by Make (repository_dispatch yt-channel,
payload {ids: "a,b", titles: "t1 ## t2"}) into yt/channel-all.json. Used for duplicate/placeholder cleanup."""
import datetime as dt, json, os
p = json.load(open(os.environ["GITHUB_EVENT_PATH"])).get("client_payload", {})
ids = [i for i in (p.get("ids") or "").split(",") if i]
titles = (p.get("titles") or "").split(" ## ")
rows = [{"id": i, "title": titles[n] if n < len(titles) else ""} for n, i in enumerate(ids)]
json.dump({"at": dt.datetime.now(dt.timezone(dt.timedelta(hours=5))).isoformat(), "videos": rows},
          open("yt/channel-all.json", "w"), indent=1, ensure_ascii=False)
print(len(rows), "videos recorded")
