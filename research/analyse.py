import json,re,statistics as st,collections,sys
d=json.load(open(sys.argv[1]))
U={'s':1/86400,'min':1/1440,'h':1/24,'d':1,'w':7,'mo':30,'y':365}
def days(a):
    m=re.search(r'(\d+)\s*(mo|min|y|w|d|h|s)\b',a or '')
    return int(m.group(1))*U[m.group(2)] if m else None
rows=collections.defaultdict(dict)
for r in d['results']: rows[(r['lang'],r['q'])][r['gl']]=r['items']
print("| Query | Lang | Top-10 median age | Share < 1 year | Lifetime-average views per day (lifetime views ÷ age), videos <1 y old, median | Distinct channels in top 10 | Top-10 overlap with US |")
print("|---|---|---|---|---|---|---|")
for (lang,q),regs in rows.items():
    allit={i['id']:i for its in regs.values() for i in its[:10]}.values()
    ages=[days(i['age']) for i in allit if days(i['age'])]
    rec=[i['views']/max(days(i['age']),1) for i in allit if i.get('views') and days(i['age']) and days(i['age'])<365]
    ids={g:[i['id'] for i in its[:10]] for g,its in regs.items()}
    ref=set(ids.get('US') or [])
    ov=st.median([len(ref & set(s))/max(len(s),1) for g,s in ids.items() if g!='US']) if ref else 0
    chans=st.median([len({i['channel'] for i in its[:10]}) for its in regs.values() if its])
    print(f"| {q} | {lang} | {int(st.median(ages))} d | {sum(a<365 for a in ages)/len(ages):.0%} | {int(st.median(rec)) if rec else 0:,} (n={len(rec)}) | {chans:g} | {ov:.0%} |")
