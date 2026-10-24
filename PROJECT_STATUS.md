# PROJECT_STATUS — Filed Under Failure

_Last updated: 2026-10-24 06:40 PKT (monitor)_

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
- 22 Oct: 005 Patisserie Valerie built (13:53, -14.5 LUFS, 71 MB), fact-checked (fixes applied), thumbnail/.srt/7 Shorts pushed to 005/; ledger rows 005-ep + 005-a (Sat 31 Oct 21:00), 005-b..g (1–6 Nov), lane api, status planned.
- `yt/native/004.md` is obsolete — do NOT upload 004 in Studio (would duplicate).

## In progress
- 004 rollout: all scheduled on YouTube except 004-g (auto-queued next).
- 005: waiting for hourly feed + 12-hourly Make run to schedule; verify videoIds in ledger, then add yt/ops.json entries (playlist pl-005, episode links).

## Blockers
- 22 Oct (monitor, social batch): FAILED at step 3: applying batch.patch (artifact YPvXAv4qjjGx224Jeb1VQY, sha256 OK, touches only social/) was denied by the sandbox auto-mode classifier [Untrusted Code Integration]; nothing pushed.
- 24 Oct (monitor): 004-g scheduled (9TKmRYB1Wo4), its ops added; 003-g public; 005 rows queued for today's Make run; no task failures; cap 23 Oct OK (23 outreach + 2 tests, 9 first-touch); FrontDesk Reel queue still empty (batch runs Sun 25 Oct 02:17).
- 23 Oct (monitor): social blocker resolved — queue has posts 23–29 Oct. YouTube all scheduled through 29 Oct; 003-f published; no ops failures; Reels queue empty (Reel batch task not enabled).
- Renderer lives in the control-room artifact (pipeline/*.py.txt); render with python3.13 + Poppins/Lora fonts from raw.githubusercontent.com/google/fonts.

## Next steps
1. Verify 005 rows become "scheduled"; add 005 ops (playlist, Full Episodes, Short links).
2. Episode 006 Wirecard (Sat 7 Nov): run demand check first (005 demand unmeasured, likely <100K).
3. Weekly update to Qazi (uploads, views, subs, YPP progress).

## Social (Xenova + FrontDesk) — 23 Oct 2026
- 90-day plan: social/calendar/calendar-90d.json (+ .csv, build_calendar.py). Weekly social batch MUST follow it (feed rows by brand/date; Fri offer, Sat carousel, Sun poll, Mon mistakes/tip, Tue comparison, Wed demo/BTS, Thu checklist; alternate dark/light per brand). Artifact: https://claude.ai/artifact/T5y6fPAw8AZVZ9QUJQ2vzA
- Feed queued through 5 Nov (posts/2026-10-30.json, 14 posts, rendered, pushed). Next batch: 6–12 Nov rows.
- Render: CHROMIUM=/opt/pw-browsers/chromium-*/chrome-linux64/chrome node studio/render.js <posts.json> "$PWD/social/img" (outDir must be ABSOLUTE).
- Blockers: Metricool free limit used until 1 Nov (Xenova FB/IG via Metricool errored 23 Oct; Make lane unaffected). Metricool YouTube = FUF channel, never post Xenova/FrontDesk there. No Xenova or FrontDesk YouTube channel connected for Shorts/long/community. Reel batch task (trig_01DokTa9hY1NLERpXhouHCJf) updated to follow the calendar and ENABLED 23 Oct (first FrontDesk calendar Reel Tue 3 Nov).
- Xenova video template: studio/xreel.js (frames) + xreel.py (Kokoro TTS bm_george, generated pad music, zoom, .srt, cover). Specs in social/xreels/. First: xv-1102 Identixa KYC, scheduled in Metricool (post 404126943) Mon 2 Nov 19:00 PKT IG+FB Reel. Xenova videos go via Metricool (20/month free); feed stays on Make.
- 23 Oct audit: Xenova video task created (trig_01SmKyKZYhcpLDMarCUsYnzi, Sat 03:41 PKT). Social batch, lead routine and job search prompts updated (calendar; named decision-makers only, shared send cap across streams; job profile Zavtech ended Oct 2026 + QA roles). Usage-limit recovery (trig_01YZVvDvN8NLBzBAD9jMV9kL) duplicates the monitor: disable pending Qazi OK. Unknown agency-partner email stream (not in cloud tasks) sends from services@. Leads: 0 human replies to date. No DMARC record on xenovasolutions.com. Reference Reel DeuKON4juZb not viewable (Instagram blocks fetch; no browser link) – waiting for file.
- 23 Oct (2): Usage-limit recovery DISABLED (monitor is the only retry path). Monitor prompt now verifies outcomes (lead report per weekday, shared send cap, bounces, unanswered replies, Reels/Metricool, feed). BoloCart task: shared 25/day cap (max 8 its own). Email auth verified via Port25 23 Oct: SPF pass, DKIM pass (xenovasolutions.com + mailbaby.net), iprev pass; DMARC p=none exists. 16–21 Oct gap: lead routine sent nothing and wrote no reports while the agency stream sent 34 (26 on 16 Oct); agency stream signs "Qazi Ihsan Ahmad", not a cloud task (likely a desktop-app task) – Qazi to locate. Browsers not linked: reference Reel + job applications blocked.
- 23 Oct (3): agency-partner stream identified by headers: sent via Gmail API by Google project 77377267392 (Claude connector = 101988054943), no display name in From. Not a Claude task. VERIFIED 23 Oct: it is Qazi's ChatGPT scheduled task "Xenova daily lead pipeline" (~07:45 PKT, Google Sheet CRM, max 5 first-touch + follow-ups/day). Do NOT revoke OpenAI; Qazi adds a cap paragraph in ChatGPT (its share: 10/day). Monitor updated to name it. Qazi capped it 23 Oct (pasted cap paragraph); check Mon 26 Oct 16:00 (trig_012p3jLV58ams3QGMg6aXbsH). Other ChatGPT tasks: "Xenova reply watch", "QA morning applications" (crowdtesting platforms e.g. uTest; no overlap with Claude job search, which covers employer roles and skips marketplaces/gigs), "Renewal Desk daily health check". Lead routine 23 Oct verified: 4 named first-touch + 9 follow-ups, report written, 23/25. 23 Oct feed posts verified live (FB/IG both brands + LI).
- YouTube for both brands: waiting on Qazi to create/connect channels (Xenova: new channel under xenovasolutionsofficial + Make eu2 YouTube connection; FrontDesk: check eu1 scenario "FDF Instagram to YouTube Shorts").

## Key files
- `yt/ledger.json`, `yt/published.json`, `yt/stats/` — state
- `NNN/NNN-<slug>.json` — episode spec (scenes, shorts, sources, notes)
- `yt/native/NNN.md` — Studio upload kit
- `.github/workflows/yt-*.yml` — automation
- `strategy/`, `research/` — topic demand research

## Playbook
- 22 Oct: Shorts hook patterns adopted (control room growth/playbook rules): 5 fact-filled patterns, no generic accusation hooks.
