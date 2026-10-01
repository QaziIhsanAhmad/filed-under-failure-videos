"""Refresh the long-lived Instagram token (valid ~60 days) and print the new one."""
import json, os, sys, urllib.request, urllib.parse, urllib.error
q = urllib.parse.urlencode({"grant_type": "ig_refresh_token",
                            "access_token": os.environ["IG_ACCESS_TOKEN"]})
try:
    with urllib.request.urlopen(f"https://graph.instagram.com/refresh_access_token?{q}", timeout=60) as r:
        d = json.load(r)
except urllib.error.HTTPError as e:
    sys.exit(f"Token refresh failed: {e.code} {e.read().decode()[:300]}")
print(f"::add-mask::{d['access_token']}")
print(f"Token refreshed; valid for {int(d.get('expires_in', 0)) // 86400} days", file=sys.stderr)
with open(os.environ["GITHUB_OUTPUT"], "a") as fh:
    fh.write(f"token={d['access_token']}\n")
