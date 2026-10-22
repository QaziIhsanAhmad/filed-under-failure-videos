# PROJECT_STATUS — Filed Under Failure

_Last updated: 2026-10-22_

## Goal
Faceless business-collapse documentary channel. Daily Short + weekly long episode, free tools only, hands-off, reach YPP honestly.

## How the pipeline runs (details: yt/SETUP-GUIDE.md)
- `yt/ledger.json` = schedule + status of every upload. GitHub job puts the day's Short in the feed at 12:00 PKT; Make uploads at 21:00 PKT; result written back to the ledger. Hourly channel check fills `yt/published.json`.
- Long episodes (>Make file limit) are uploaded by Qazi in Studio from `yt/native/NNN.md` (about 5 min).
- Daily stats: `yt/stats/yt-stats-YYYY-MM-DD.json`.

## Done
- Episodes 001–003 + Shorts published (17 published items, ~2.5K total views across 25 videos as of 21 Oct).
- 003 Shorts f/g scheduled for 22–23 Oct.
- 004 Northern Rock: long video (15:14), thumbnail, .srt, 7 Shorts rendered; independent fact-check done 22 Oct (0 wrong).
- `yt/native/004.md` upload kit created 22 Oct.

## In progress
- 004 rollout: long episode Sat 24 Oct (Qazi, Studio); Shorts 004-a…g auto 24–30 Oct.

## Blockers
- Needs Qazi: upload 004 long episode in Studio by Sat 24 Oct 21:00 PKT using `yt/native/004.md`.
- Renderer (TTS Kokoro bm_george + scene→mp4 + Shorts) is NOT in this repo; only outputs are. Must be rebuilt or committed before episode 005 can be produced.

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
