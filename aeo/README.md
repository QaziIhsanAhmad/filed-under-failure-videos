# Xenova AEO toolkit

- `aeo_audit.py` — free crawler/audit (robots AI-bot access, indexability, snippets, schema, titles, internal links, thin pages, speed). Runs monthly via GitHub Actions (`.github/workflows/aeo-audit.yml`) and writes `reports/YYYY-MM.{json,html}` + `reports/latest.*`.
- `questions.json` — the 25 fixed buyer questions tracked every month.
- `baseline-2026-09-30.json` — starting point. Monthly results go in `scorecards/YYYY-MM.json`.

No tool can guarantee rankings or AI citations; these files measure eligibility and trend.
