"""Collects the latest UK Smart Data company announcements. Run by GitHub Actions."""
import json, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from rules import QUERIES
from scoring import record
from companies_house import enrich

OUT = Path(__file__).parent / "announcements.json"
UA = "Mozilla/5.0 (compatible; DBT-SmartData-Scanner/2.0; news feeds only)"

def feeds(q):
    yield "Google News", "https://news.google.com/rss/search?q=" + urllib.parse.quote(q + " when:14d") + "&hl=en-GB&gl=GB&ceid=GB:en"
    yield "Bing News", "https://www.bing.com/news/search?format=rss&setmkt=en-GB&q=" + urllib.parse.quote(q)

def read(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        root = ET.fromstring(r.read())
    for it in root.iter("item"):
        title = " ".join(unescape(it.findtext("title") or "").split())
        desc = " ".join(re.sub(r"<[^>]+>", " ", unescape(it.findtext("description") or "")).split())
        if desc[:40] == title[:40]: desc = ""
        try: date = parsedate_to_datetime(it.findtext("pubDate")).date().isoformat()
        except Exception: date = time.strftime("%Y-%m-%d")
        src = it.findtext("source") or ""
        if not src:
            m = re.search(r"\s[-|–]\s([^-|–]{2,60})$", title); src = m.group(1) if m else ""
        yield title, desc, (it.findtext("link") or "").strip(), date, src

def main():
    OUT.parent.mkdir(exist_ok=True)
    try: store = {r["id"]: r for r in json.loads(OUT.read_text(encoding="utf-8"))["items"]}
    except Exception: store = {}
    read_n = new = fails = 0
    for q in QUERIES:
        for engine, url in feeds(q):
            try:
                for title, desc, link, date, src in read(url):
                    read_n += 1
                    r = record(title, desc, link, date, src or engine, q)
                    if r and r["id"] not in store:
                        store[r["id"]] = enrich(r); new += 1
            except Exception as e:
                fails += 1; print("feed failed:", engine, q, e)
            time.sleep(0.7)
    items = sorted(store.values(), key=lambda r: (r["date"], r["score"]), reverse=True)
    OUT.write_text(json.dumps({"updated": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "last_run": {"searches": len(QUERIES) * 2, "failed": fails, "headlines_read": read_n, "new": new},
        "items": items}, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"Read {read_n} headlines, {fails} feeds failed, {new} new Smart Data announcements, {len(items)} in total.")
    if read_n == 0: raise SystemExit("Nothing could be read - feeds blocked or unreachable.")

if __name__ == "__main__":
    main()
