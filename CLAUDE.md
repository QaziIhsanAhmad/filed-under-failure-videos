# Working rules (token budget)

1. Start every session by reading `PROJECT_STATUS.md`. Do not scan the whole repo or replay history.
2. Read only files listed in "Key files" or directly needed for the task. Use grep/glob before opening large files.
3. No repeated checks, no full logs — tail/grep output to the relevant lines.
4. Run tests only when code changes require them; run the narrowest test that covers the change.
5. After meaningful progress, update `PROJECT_STATUS.md` (Done / In progress / Blockers / Next steps, date). Keep it under ~60 lines.
6. Keep replies short: what changed, what's next, anything that needs me.
