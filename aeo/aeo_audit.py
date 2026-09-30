#!/usr/bin/env python3
"""AEO/SEO site audit: crawl a site (sitemap-first), check AI-search readiness, write JSON + HTML report.

Usage: python aeo_audit.py https://example.com [--max 150] [--out report]
Free, no API keys. Needs: pip install requests beautifulsoup4 lxml
"""
import argparse, json, re, sys, time, datetime as dt
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 (compatible; XenovaAEOAudit/1.0; +https://xenovasolutions.com)"
AI_BOTS = ["OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User",
           "Claude-SearchBot", "Claude-User", "ClaudeBot", "Google-Extended", "Googlebot", "Bingbot", "Applebot-Extended", "CCBot"]
SEARCH_BOTS = {"OAI-SearchBot", "PerplexityBot", "Claude-SearchBot", "Googlebot", "Bingbot"}
S = requests.Session(); S.headers["User-Agent"] = UA


def get(url, **kw):
    try:
        return S.get(url, timeout=25, allow_redirects=True, **kw)
    except requests.RequestException as e:
        return None


def robots_rules(base):
    r = get(urljoin(base, "/robots.txt"))
    txt = r.text if r is not None and r.ok else ""
    groups, cur, agents = {}, [], []
    for line in txt.splitlines():
        line = line.split("#")[0].strip()
        if not line or ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if cur:  # new group
                agents, cur = [], []
            agents.append(v.lower())
            for a in agents:
                groups.setdefault(a, [])
        elif k in ("allow", "disallow"):
            cur.append((k, v))
            for a in agents:
                groups[a] = cur
    def blocked(bot):
        rules = groups.get(bot.lower(), groups.get("*", []))
        return any(k == "disallow" and v == "/" for k, v in rules) and not any(k == "allow" and v == "/" for k, v in rules)
    sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", txt)
    return txt, {b: ("blocked" if blocked(b) else "allowed") for b in AI_BOTS}, sitemaps


def sitemap_urls(sm_urls, limit):
    seen, out, queue = set(), [], list(sm_urls)
    while queue and len(out) < limit:
        sm = queue.pop(0)
        if sm in seen:
            continue
        seen.add(sm)
        r = get(sm)
        if r is None or not r.ok:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
        if "<sitemapindex" in r.text:
            queue.extend(locs)
        else:
            out.extend(locs)
    return list(dict.fromkeys(out))[:limit]


def jsonld_types(soup):
    types = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except Exception:
            types.append("INVALID_JSON")
            continue
        items = data if isinstance(data, list) else data.get("@graph", [data]) if isinstance(data, dict) else []
        for it in items:
            t = it.get("@type") if isinstance(it, dict) else None
            types.extend(t if isinstance(t, list) else [t] if t else [])
    return types


def audit_page(url, host):
    t0 = time.time(); r = get(url); ms = int((time.time() - t0) * 1000)
    row = {"url": url, "status": r.status_code if r is not None else 0, "ms": ms, "issues": []}
    if r is None or not r.ok or "html" not in r.headers.get("content-type", ""):
        row["issues"].append("not reachable / not HTML"); return row, []
    soup = BeautifulSoup(r.text, "lxml")
    title = (soup.title.string or "").strip() if soup.title else ""
    md = soup.find("meta", attrs={"name": "description"})
    desc = md.get("content", "").strip() if md else ""
    robots = soup.find("meta", attrs={"name": "robots"})
    robots_c = (robots.get("content", "") if robots else "").lower()
    xrobots = r.headers.get("x-robots-tag", "").lower()
    canon = soup.find("link", rel="canonical")
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    main = soup.find("main") or soup.body or soup
    text = main.get_text(" ", strip=True)
    words = len(text.split())
    links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
    internal = [l.split("#")[0] for l in links if urlparse(l).netloc == host]
    external = [l for l in links if urlparse(l).netloc and urlparse(l).netloc != host]
    imgs = soup.find_all("img"); no_alt = [i for i in imgs if not i.get("alt")]
    types = jsonld_types(soup)
    has_date = bool(soup.find("time") or soup.find("meta", attrs={"property": "article:modified_time"})) or "dateModified" in r.text
    has_table = bool(main.find("table")); has_list = bool(main.find(["ol", "ul"]))
    qs = [h.get_text(" ", strip=True) for h in main.find_all(["h2", "h3"]) if h.get_text().strip().endswith("?")]
    row.update(title=title, title_len=len(title), desc_len=len(desc), h1=len(h1s), words=words,
               internal_links=len(set(internal)), external_links=len(set(external)), img_no_alt=len(no_alt),
               schema=types, canonical=canon.get("href") if canon else "", question_headings=len(qs),
               has_table=has_table, has_date=has_date)
    iss = row["issues"]
    if "noindex" in robots_c or "noindex" in xrobots: iss.append("noindex (not eligible for search or AI answers)")
    if "nosnippet" in robots_c or "max-snippet:0" in robots_c: iss.append("snippets blocked (not eligible for AI Overview citation)")
    if not title: iss.append("missing title")
    elif len(title) > 65: iss.append("title over 65 chars")
    if not desc: iss.append("missing meta description")
    if len(h1s) != 1: iss.append(f"{len(h1s)} H1 tags")
    if not canon: iss.append("no canonical")
    if not types: iss.append("no structured data")
    if "INVALID_JSON" in types: iss.append("invalid JSON-LD")
    if words < 300: iss.append("thin content (<300 words)")
    if len(set(internal)) < 3: iss.append("fewer than 3 internal links")
    if no_alt: iss.append(f"{len(no_alt)} images without alt")
    if ms > 2500: iss.append(f"slow HTML response ({ms} ms)")
    return row, internal


def score(pages, bots):
    pts, total = 0, 0
    for b in SEARCH_BOTS:
        total += 4; pts += 4 if bots.get(b) == "allowed" else 0
    for p in pages:
        total += 10; pts += max(0, 10 - 2 * len(p["issues"]))
    return round(100 * pts / total) if total else 0


def html_report(site, data):
    rows = "".join(
        f"<tr><td><a href='{p['url']}'>{p['url'].replace(site,'') or '/'}</a></td><td>{p.get('words','')}</td>"
        f"<td>{', '.join(sorted(set(p.get('schema', [])))) or '—'}</td><td>{p.get('internal_links','')}</td>"
        f"<td>{p['ms']}</td><td>{'<br>'.join(p['issues']) or 'OK'}</td></tr>" for p in data["pages"])
    bots = "".join(f"<tr><td>{b}</td><td>{s}</td></tr>" for b, s in data["bots"].items())
    return f"""<!doctype html><meta charset=utf-8><title>AEO audit – {site}</title>
<style>body{{font:15px/1.5 system-ui;margin:24px;max-width:1100px}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:6px;vertical-align:top;font-size:13px}}th{{background:#f3f3f3;text-align:left}}</style>
<h1>AI Search Readiness Audit</h1><p><b>{site}</b> · {data['date']} · Score <b>{data['score']}/100</b> · {len(data['pages'])} pages</p>
<h2>AI and search crawler access (robots.txt)</h2><table><tr><th>Bot</th><th>Status</th></tr>{bots}</table>
<h2>Top issues</h2><ul>{''.join(f'<li>{k}: {v} pages</li>' for k, v in data['top_issues'])}</ul>
<h2>Pages</h2><table><tr><th>Page</th><th>Words</th><th>Schema</th><th>Internal links</th><th>HTML ms</th><th>Issues</th></tr>{rows}</table>
<p style="color:#666">Checks eligibility and clarity signals only. No tool can guarantee AI citations or rankings.</p>"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("site"); ap.add_argument("--max", type=int, default=150)
    ap.add_argument("--out", default="aeo-report"); a = ap.parse_args()
    site = a.site.rstrip("/"); host = urlparse(site).netloc
    robots_txt, bots, sms = robots_rules(site)
    urls = sitemap_urls(sms or [site + "/wp-sitemap.xml", site + "/sitemap.xml", site + "/sitemap_index.xml"], a.max) or [site + "/"]
    if site + "/" not in urls: urls.insert(0, site + "/")
    pages, linked = [], set()
    for u in urls:
        row, internal = audit_page(u, host); pages.append(row); linked.update(internal); time.sleep(0.5)
    for p in pages:
        if p["url"] != site + "/" and p["url"] not in linked and p["url"].rstrip("/") not in {l.rstrip("/") for l in linked}:
            p["issues"].append("orphan (no internal links found to it)")
    counts = {}
    for p in pages:
        for i in p["issues"]:
            k = re.sub(r"\d+", "N", i); counts[k] = counts.get(k, 0) + 1
    data = {"site": site, "date": dt.date.today().isoformat(), "bots": bots, "sitemaps": sms,
            "score": score(pages, bots), "top_issues": sorted(counts.items(), key=lambda x: -x[1])[:10], "pages": pages}
    json.dump(data, open(a.out + ".json", "w"), indent=1)
    open(a.out + ".html", "w").write(html_report(site, data))
    print(json.dumps({k: data[k] for k in ("site", "date", "score", "top_issues", "bots")}, indent=1))


if __name__ == "__main__":
    main()
