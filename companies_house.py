"""Fills HQ, what the company does and size automatically from the official Companies House API.
Only runs if the free key is saved as the repo secret COMPANIES_HOUSE_API_KEY."""
import os, json, base64, urllib.request, urllib.parse
KEY = os.environ.get("COMPANIES_HOUSE_API_KEY", "")
SIZE = {"micro-entity": "Micro", "small": "Small", "total-exemption-small": "Small", "total-exemption-full": "Small/Medium",
        "unaudited-abridged": "Small", "medium": "Medium", "full": "Medium/Large", "group": "Large (group)"}
SIC = {"62": "Software / IT services", "63": "Data processing / information services", "64": "Banking / financial services",
       "65": "Insurance / pensions", "66": "Financial services support", "68": "Real estate", "35": "Energy supply",
       "47": "Retail", "61": "Telecommunications", "49": "Transport", "52": "Transport support", "69": "Legal / accounting",
       "70": "Consultancy", "72": "Research", "73": "Advertising / market research", "82": "Business support",
       "01": "Agriculture", "10": "Food manufacturing", "58": "Publishing / software"}
_cache = {}

def _get(path):
    req = urllib.request.Request("https://api.company-information.service.gov.uk" + path)
    req.add_header("Authorization", "Basic " + base64.b64encode((KEY + ":").encode()).decode())
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)

def enrich(rec):
    name = rec.get("company")
    if not KEY or not name: return rec
    if name not in _cache:
        info = {}
        try:
            items = [i for i in _get("/search/companies?items_per_page=5&q=" + urllib.parse.quote(name)).get("items", [])
                     if i.get("company_status") == "active"]
            if items:
                num = items[0]["company_number"]; p = _get(f"/company/{num}")
                a = p.get("registered_office_address", {})
                codes = p.get("sic_codes", [])
                info = {"hq": a.get("locality", "") or a.get("postal_code", ""),
                        "what_it_does": ", ".join(dict.fromkeys(SIC.get(c[:2], "SIC " + c) for c in codes)),
                        "size": SIZE.get(p.get("accounts", {}).get("last_accounts", {}).get("type", ""), ""),
                        "turnover": "See filed accounts",
                        "companies_house": f"https://find-and-update.company-information.service.gov.uk/company/{num}",
                        "registered_name": p.get("company_name", "")}
        except Exception as e:
            print("Companies House lookup failed:", name, e)
        _cache[name] = info
    rec.update(_cache[name])
    return rec
