import re, hashlib
from rules import SIGNALS, SECTORS, EXCLUDE, NON_UK, UK, KEEP_FROM
SIG = [(p, re.compile(rx, re.I), lab) for p, rx, lab in SIGNALS]
VERBS = r"(?:launch|partner|rais|team|unveil|roll|expand|acquir|join|introduc|go|secur|integrat|select|announc|add|bring|open|win|sign|debut|back|tap|use|enabl|offer|power|deploy|complet|hit|reach|become|cut|let|make|help|start|receiv|land|bag|clos|gain|extend|appoint|award)"

GENERIC = {"uk","the","new","british","government","why","how","what","lender","lenders","fintech","fintechs","bank","banks","startup","start-up","firm","firms","app","drivers","customers","consumers","regulator","insurer","broker","platform","report","study","survey","energy firms","households","landlords","tenants","shoppers","homebuyers","councils","minister","ministers","this","it","new app","scheme"}

def clean_title(t):
    return re.sub(r"\s+[-|–]\s+[^-|–]{2,60}$", "", t).strip()

def company(title):
    t = clean_title(title)
    m = re.match(r"^((?:[A-Z0-9][\w&.'’+\-]*)(?:\s+(?:[A-Z0-9][\w&.'’+\-]*|&|and|of))*?)(?:'s|’s)?\s+" + VERBS, t)
    if m and m.group(1).lower() not in GENERIC:
        return m.group(1).strip()
    m = re.search(r"\b(?:partnership (?:between|with)|teams up with|partners with|backed by|acquired by|selected by|chosen by)\s+([A-Z][\w&.'’+\-]*(?:\s+[A-Z][\w&.'’+\-]*){0,2})", t)
    return m.group(1) if m else ""

def assess(title, summary):
    text = f"{title}. {summary}"
    if re.search(EXCLUDE, text, re.I):
        return None
    pts, uses = 0, []
    for p, rx, lab in SIG:
        if rx.search(text):
            pts += p
            if lab and lab not in uses: uses.append(lab)
    if re.search(NON_UK, text, re.I) and not re.search(UK, text, re.I):
        pts -= 4
    if re.search(UK, text, re.I): pts += 1
    sector, best = "Cross-sector", 0
    for s, rx in SECTORS.items():
        n = len(re.findall(rx, text, re.I))
        if n > best: sector, best = s, n
    if not uses or pts < KEEP_FROM:
        return None
    return pts, sector, uses

def record(title, summary, link, date, source, how):
    a = assess(title, summary)
    if not a: return None
    pts, sector, uses = a
    key = re.sub(r"[^a-z0-9 ]", "", clean_title(title).lower())
    return {"id": hashlib.sha1(key.encode()).hexdigest()[:12], "date": date, "company": company(title),
            "what_it_does": "", "how_it_uses_smart_data": "; ".join(uses[:2]), "hq": "", "size": "", "turnover": "",
            "sector": sector, "headline": clean_title(title), "summary": summary[:300], "source": source,
            "url": link, "score": pts, "found_by": how}
