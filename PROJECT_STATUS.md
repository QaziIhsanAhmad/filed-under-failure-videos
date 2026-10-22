# PROJECT_STATUS — Filed Under Failure

_Last updated: 2026-10-22 (14:10 PKT)_

## Goal
Faceless business-collapse documentary channel. Daily Short + weekly long episode, free tools only, hands-off, reach YPP honestly.

## How the pipeline runs (details: yt/SETUP-GUIDE.md)
- `yt/ledger.json` = schedule + status of every upload. GitHub job puts the day's Short in the feed at 12:00 PKT; Make uploads at 21:00 PKT; result written back to the ledger. Hourly channel check fills `yt/published.json`.
- Since 15 Oct ALL uploads (episodes too, any size) go through lane "api" (yt/yt_api.py): hourly feed queues rows due within 8 days; Make "FUF upload sessions (API lane)" uploads them private with publishAt = slot. No Studio kits needed.
- Daily stats: `yt/stats/yt-stats-YYYY-MM-DD.json`.

## Done
- Episodes 001–003 + Shorts published (17 published items, ~2.5K total views across 25 videos as of 21 Oct).
- 003 Shorts f/g scheduled for 22–23 Oct.
- 004 Northern Rock: long video (15:14), thumbnail, .srt, 7 Shorts rendered; independent fact-check done 22 Oct (0 wrong).
- 22 Oct: 004-ep + Shorts a–f uploaded via API lane, private, scheduled (ep sKaLC6A0Igw + a 9kHvzWHymns Sat 24 Oct 21:00 PKT; b–f 25–29 Oct). 004-g (30 Oct) queues automatically within 8 days of its slot.
- 22 Oct (monitor): added yt/ops.json ops for 004 (playlist pl-004, Full Episodes item, episode links in Shorts a–f) and 003-g; 004-g ops still to add once it has a videoId.
- `yt/native/004.md` is obsolete — do NOT upload 004 in Studio (would duplicate).

## In progress
- 004 rollout: all scheduled on YouTube except 004-g (auto-queued next).

## Blockers
- 22 Oct 14:10 (monitor): social/queue.json has no posts after 22 Oct; social batch ran twice today (incl. monitor retry 13:44) but pushed nothing — Qazi to check. YouTube OK through 29 Oct (004-g queues automatically).
- Renderer lives in the control-room artifact (pipeline/*.py.txt); render with python3.13 + Poppins/Lora fonts from raw.githubusercontent.com/google/fonts.

## Next steps
1. Episode 005: pick topic passing the demand rule (top-10 median ≥100K views; 004 was below it), research from primary records, write `005/005-<slug>.json` in the 004 spec format.
2. Rebuild + commit renderer under `tools/` so future episodes are reproducible; render 005 + Shorts; add ledger entries from 31 Oct.
3. Weekly update to Qazi (uploads, views, subs, YPP progress).

## Key files
- `yt/ledger.json`, `yt/published.json`, `yt/stats/` — state
- `NNN/NNN-<slug>.json` — episode spec (scenes, shorts, sources, notes)
- `yt/native/NNN.md` — Studio upload kit
- `.github/workflows/yt-*.yml` — automation
- `strategy/`, `research/` — topic demand research

## Playbook
- 22 Oct: Shorts hook patterns adopted (control room growth/playbook rules): 5 fact-filled patterns, no generic accusation hooks.
