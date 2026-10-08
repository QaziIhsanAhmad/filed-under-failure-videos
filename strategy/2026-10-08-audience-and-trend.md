# Audience, language and trend research (8 Oct 2026)

## CPM is not RPM
- CPM = what advertisers pay per 1,000 ad impressions. RPM = what the creator receives per 1,000 views, after YouTube's share and after views that show no ad.
- Third-party estimates (videodubbing.com, Aug 2026; creator-reported, not official): long-form RPM US $9-11, UK $6-7, Canada $8-10, Australia $10-12, UAE $2.50-4, India $0.40-1, Pakistan $0.20-0.50, Bangladesh $0.20-0.40.
- Shorts RPM is far lower (AIR Media-Tech 2025 data): US $0.33, UK $0.17, Canada $0.17, Australia $0.19, India $0.008.
- These are market averages, not a forecast for this channel. Our real RPM is unknown until the channel is monetised.
- YouTube's official pages do not publish revenue-share percentages, so none are quoted here.

## Watch hours are not country-restricted
- YPP: 1,000 subscribers + 4,000 public long-form watch hours (12 months) or 10M Shorts views (90 days). The official page sets no viewer-country limit; the creator must live where YPP is available, and Pakistan, India and Bangladesh are on YouTube's list.

| Factor | English (US/UK/CA/AU + global English speakers) | Urdu/Hindi (Pakistan, India, Gulf diaspora) |
|---|---|---|
| Demand | 259M US + 57M UK YouTube users; business-documentary channels reach 1-5M subs (MagnatesMedia, Company Man, How Money Works) | 518M India + 59M Pakistan users; Think School alone: 6.6M subs, ~0.94M avg views (Qoruz, Oct 2026) |
| Competition | Crowded at the top, but specific collapse stories and post-mortems are underserved (faceless.my, Jun 2026) | Dominated by large presenter-led channels; few faceless, source-cited ones |
| Language fit | Native English TTS voice already tested; scripts and fact-checks done in English | Qazi is a native Urdu speaker (can judge scripts); free Hindi TTS pronunciation not yet verified by ear; no Devanagari font installed (Roman captions only) |
| Retention risk | Low-medium (natural British voice) | Unknown until a native listener confirms the voice |
| Subscriber potential | Moderate; slower growth, higher value per viewer | High reach, but ~10-40x lower RPM per view |
| Verdict | Keep as the main channel | Test on a separate channel only after the voice passes a listening check |

## Trend concept (recommended): news-pegged collapse Shorts from the official record
- Evidence: Shorts are the fastest discovery route for channels under 10k subscribers (Metricool study of 799,718 videos). Timely topics bring search demand. A24's Theranos/Elizabeth Holmes documentary "You Can See Everything" opens in US cinemas on 16 Oct 2026 with wide coverage (NYT, Newsweek, AP); the film is a personal portrait, so "what the court actually found" is an open angle.
- Seven-day pilot (main channel, English):
  - Fri 16 Oct 18:00 PKT: release-day Short (if the episode is ready in time)
  - Sat 17 Oct 18:00 PKT: teaser Short; 21:00 PKT: Theranos episode
  - Sun 18 to Fri 23 Oct 21:00 PKT: six Theranos Shorts, each a different court/regulator fact
- Success measures (from YouTube analytics via Metricool, judged after 7 full days): views per Short vs SVB week (control), % viewed, subscribers gained per 1,000 views, share of episode traffic from YouTube search. Continue news pegs if Theranos beats SVB on views per Short by 30%+.

## Preliminary evidence (8 Oct 2026 snapshot): treat as indicative, not proof
Method: a GitHub Action collected the top 20 logged-out YouTube search results for 12 content queries (5 English, 4 Hindi, 3 Urdu), region set to US, GB, CA, AU, IN, PK, BD, AE (Hindi/Urdu: IN, PK, AE, US). Data: research/yt-search-2026-10-08.json; analysis: research/analyse.py.
Limits: one day; logged-out search only (not recommendations or Shorts feed, where most new-channel views come from); lifetime views of surviving top results; "views per day" = lifetime views / age, which overstates older spikes; no subscriber, retention or search-volume data; small n for some rows.

| Query | Lang | Top-10 median age | Share < 1 year | Recent (<1 y) median views/day | Distinct channels in top 10 | Top-10 overlap with US |
|---|---|---|---|---|---|---|
| silicon valley bank collapse explained | en | 1095 d | 15% | 288 (n=2) | 9 | 90% |
| theranos documentary | en | 150 d | 57% | 46,872 (n=8) | 10 | 80% |
| carillion collapse | en | 2190 d | 38% | 1 (n=8) | 9.5 | 90% |
| company collapse documentary | en | 912 d | 27% | 579 (n=6) | 9 | 60% |
| why did this company fail | en | 730 d | 24% | 432 (n=6) | 10 | 70% |
| silicon valley bank collapse hindi | hi | 1095 d | 7% | 189,778 (n=1) | 10 | 70% |
| theranos hindi | hi | 1277 d | 17% | 4 (n=2) | 10 | 100% |
| business case study hindi | hi | 90 d | 71% | 7,575 (n=10) | 5.5 | 80% |
| company kyu doob gayi | hi | 150 d | 54% | 604 (n=7) | 9 | 90% |
| silicon valley bank urdu | ur | 1095 d | 0% | 0 (n=0) | 10 | 80% |
| business case study urdu | ur | 365 d | 31% | 87 (n=4) | 8 | 90% |
| company collapse urdu | ur | 547 d | 38% | 5,240 (n=6) | 10 | 70% |


Reading it carefully:
- Current demand: "theranos documentary" is the only English query with mostly recent results (57% under 1 year, median ~47K views/day), consistent with interest building before the 16 Oct film. SVB and Carillion queries are dominated by old videos with low recent views/day, so their current search demand looks weak (SVB's Saturday episode should be judged with that in mind).
- Competition: English top 10s hold 9-10 different channels including major outlets (WSJ, Yahoo Finance, Entertainment Tonight); "business case study hindi" is concentrated in ~5-6 channels with mostly recent uploads (71% under 1 year, ~7.6K views/day), i.e. an active market led by a few strong channels.
- Country: top-10 overlap with the US result set is 60-100%, so logged-out search looks similar across these regions; this does NOT show country is irrelevant (recommendations, language settings and Shorts distribution can differ). Country effects should be read from our own YouTube Analytics after the pilot.
- Urdu-labelled queries show little recent activity except "company collapse urdu" (~5K views/day, small n).

Pilot choice: Theranos week (English), because it is the only option with clear current demand and a dated news peg. Judge it with the playbook evaluation rules (medians; % viewed; subscribers per 1,000 views; traffic source; country split; under 2x = inconclusive; repeat before concluding).
