"""Viewer-safe YouTube text. Every upload path calls clean_description() right before the API call.

Internal pipeline text (QA notes, approvals, OAuth/scope details, channel IDs, hashes, file paths, ledger
or operator notes) must never reach a public description. Lines that look internal are removed; if anything
leaky is still left after that, the upload is refused (fail closed) instead of publishing it.
"""
import re

_LINE_PATTERNS = [
    r"\bQA\b", r"\bquality[- ]?(check|gate|review)\b", r"\btest (note|run|upload|output)s?\b", r"\binternal\b",
    r"\bapprov(al|ed by|e before)\b", r"\boperator\b", r"\bledger\b", r"\breconcil", r"\bverified_at\b",
    r"\boauth\b", r"\bscopes?\b.*(youtube|google|auth)", r"\b(access|refresh)[_ ]token\b", r"\bclient[_ ](id|secret)\b",
    r"\bapi[_ ]?key\b", r"\bcredential", r"\btoken\.json\b", r"\bsecrets?/", r"googleapis\.com/auth",
    r"\bUC[\w-]{22}\b", r"\bchannel[_ ]id\b", r"\bsha-?(1|256)\b", r"\b[0-9a-f]{32,}\b", r"nexora-direct-",
    r"(/Users/|/home/|~/|[A-Za-z]:\\\\)", r"\bdo not publish\b", r"\bdraft only\b", r"\bTODO\b", r"\bFIXME\b",
    r"\bprivacyStatus\b", r"\bselfDeclared", r"\bcontainsSyntheticMedia\b", r"\bupload (marker|session|lane)\b",
]
_RX = re.compile("|".join(_LINE_PATTERNS), re.IGNORECASE)


class UnsafeDescription(ValueError):
    pass


def leaks(text):
    """Return the internal-looking lines in text (empty list = viewer-safe)."""
    return [ln for ln in (text or "").splitlines() if _RX.search(ln)]


def clean_description(text, limit=4900):
    """Drop internal lines, collapse blank runs, refuse if anything leaky survives."""
    kept = [ln for ln in (text or "").splitlines() if not _RX.search(ln)]
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()
    if leaks(out):
        raise UnsafeDescription("description still contains internal text; upload refused")
    if not out:
        raise UnsafeDescription("description is empty after removing internal text; upload refused")
    return out[:limit]


def clean_title(text):
    t = (text or "").strip()
    if leaks(t):
        raise UnsafeDescription("title contains internal text; upload refused")
    return t
