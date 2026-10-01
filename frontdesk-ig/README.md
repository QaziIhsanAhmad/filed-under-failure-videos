# FrontDesk Flows Instagram queue

`.github/workflows/frontdesk-instagram.yml` publishes posts for @frontdeskflows.

- Add a post: commit a JSON file to `queue/` (format in `post.py`). Media must be public URLs, e.g. files in `media/` via raw.githubusercontent.com.
- Every hour the workflow publishes at most one post whose `publish_after` time has passed and moves it to `posted/` with its Instagram link.
- Every Monday it refreshes the access token (tokens last ~60 days). Saving the refreshed token needs the optional `GH_PAT` secret; without it the old token keeps working until it expires.

Secrets: `IG_ACCESS_TOKEN`, `IG_USER_ID`, optional `GH_PAT` (fine-grained token, this repo only, "Secrets: read and write").
