"""One-off research: top YouTube search results per query and country (public pages, light use)."""
import json, re, time, urllib.parse, urllib.request, datetime as dt
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36", "Accept-Language": "en"}
QUERIES = {
 "en": ["silicon valley bank collapse explained", "theranos documentary", "carillion collapse", "company collapse documentary", "why did this company fail"],
 "hi": ["silicon valley bank collapse hindi", "theranos hindi", "business case study hindi", "company kyu doob gayi"],
 "ur": ["silicon valley bank urdu", "business case study urdu", "company collapse urdu"],
}
REGIONS = ["US", "GB", "CA", "AU", "IN", "PK", "BD", "AE"]
def views(t):
    m = re.search(r"([\d.,]+)\s*([KMB]?)", t or "")
    if not m: return None
    n = float(m.group(1).replace(",", "")); return int(n * {"": 1, "K": 1e3, "M": 1e6, "B": 1e9}[m.group(2)])
out = {"date": dt.date.today().isoformat(), "results": []}
for lang, qs in QUERIES.items():
    for q in qs:
        regions = REGIONS if lang == "en" else ["IN", "PK", "AE", "US"]
        for gl in regions:
            url = "https://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": q, "gl": gl, "hl": "en"})
            try:
                html = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30).read().decode("utf-8", "ignore")
            except Exception as e:
                out["results"].append({"q": q, "gl": gl, "error": str(e)}); continue
            items = []
            for m in re.finditer(r'"videoRenderer":\{"videoId":"([\w-]{11})"', html):
                seg = html[m.start(): m.start() + 6000]
                g = lambda p: (re.search(p, seg) or [None, None])[1]
                items.append({"id": m.group(1), "title": g(r'"title":\{"runs":\[\{"text":"(.*?)"'),
                              "channel": g(r'"ownerText":\{"runs":\[\{"text":"(.*?)"'),
                              "views": views(g(r'"viewCountText":\{"simpleText":"(.*?)"')),
                              "age": g(r'"publishedTimeText":\{"simpleText":"(.*?)"'),
                              "length": g(r'"lengthText":\{"accessibility":.*?"simpleText":"(.*?)"')})
                if len(items) >= 20: break
            out["results"].append({"lang": lang, "q": q, "gl": gl, "items": items})
            time.sleep(2)
json.dump(out, open(f"research/yt-search-{out['date']}.json", "w"), ensure_ascii=False, indent=1)
print(sum(len(r.get("items", [])) for r in out["results"]), "items")
