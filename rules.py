"""What counts as Smart Data, written as the ways companies actually phrase it.
Based on: Smart Data Definition and Scope (Saira Madden), Smart Data Guidebook Glossary
(Richard Black), Smart Data 2035 sectors. Health is excluded. You should not need to edit this."""

# 1. Searches run every time. Most avoid the words "smart data" because companies rarely use them.
QUERIES = [
 # explicit scheme language
 '"smart data" UK', '"open banking" UK', '"open finance" UK', '"pay by bank"', '"variable recurring payments"',
 '"Fuel Finder"', '"data portability" UK', '"pensions dashboard"', '"digital property pack"', '"smart meter data"',
 # how firms describe customer-permissioned data without naming it
 '"connect your bank account" app UK', '"link your bank account" UK', '"with customer consent" data UK',
 '"customer-permissioned" OR "consumer-permissioned" data', '"bank transaction data" lender UK',
 '"affordability checks" "bank data"', '"income verification" open banking', '"cash flow" lending "bank data" UK',
 '"rent reporting" credit score UK', '"account-to-account payments" UK', '"instant bank payments" launch UK',
 '"categorised transaction data"', '"energy usage data" app UK', '"half-hourly data" energy UK',
 '"switch energy supplier" data app', '"tariff comparison" "smart meter"', '"upfront information" property',
 '"material information" property data', '"property logbook"', '"conveyancing" "data sharing" UK',
 '"export your data" OR "transfer your data" platform UK', '"real-time fuel prices" UK',
 '"chargepoint data" OR "EV charging data" UK', '"mobile usage data" switching UK', '"broadband switching" data UK',
 '"farm data" sharing UK', '"loyalty data" consent UK', '"digital receipts" data UK',
 '"accounting data" lender integration UK', '"data sharing" consumers fintech UK',
]

# 2. Phrases that mean Smart Data (regex). Points, plain-English label used in "How it uses Smart Data".
SIGNALS = [
 (4, r"\bsmart data\b", "Smart Data (named directly)"),
 (4, r"\bopen banking\b", "Open banking: customer-permissioned bank data"),
 (4, r"\bopen finance\b", "Open finance: customer-permissioned financial data"),
 (4, r"\bpay(?:ing)? by bank\b|\bvariable recurring payments?\b|\bvrps?\b|\bpayment initiation\b", "Bank payments made with customer permission (open banking)"),
 (4, r"\baccount information service|\baisp?\b", "Account information access (open banking)"),
 (4, r"\bfuel finder\b", "Fuel Finder: shared fuel price data"),
 (4, r"\bdata portability\b", "Customers moving their data between services"),
 (4, r"\bpensions? dashboards?\b", "Pensions dashboard: customer-requested pension data"),
 (4, r"\bdigital property packs?\b|\bproperty logbooks?\b|\bupfront (?:property )?information\b|\bmaterial information\b", "Property data shared up front (homebuying)"),
 (4, r"\bsmart meter data\b|\bhalf[- ]hourly (?:meter |energy |usage )?data\b|\bconsumer consent solution\b", "Customer energy usage data (smart meters)"),
 (4, r"\b(?:customer|consumer|user)[- ]permissioned\b|\bpermissioned data\b|\bconsented data\b", "Customer-permissioned data"),
 (3, r"\b(?:connect|link|sync)(?:s|ing|ed)? (?:your|their|customers?'?|users?'?) (?:bank|current|savings|energy|pension|financial)? ?accounts?\b", "Customers connect their accounts to share data"),
 (3, r"\bwith (?:your|their|the customer'?s?|users?'?|explicit) (?:permission|consent)\b", "Data used with the customer's permission"),
 (3, r"\b(?:securely )?shar(?:e|es|ing) (?:your|their) (?:own )?(?:bank |financial |energy |usage |transaction )?data\b", "Customers share their own data"),
 (3, r"\b(?:bank|banking|transaction|transactional) data\b", "Uses customer bank / transaction data"),
 (3, r"\b(?:affordability|income) (?:checks?|verification|assessments?)\b", "Bank data for affordability or income checks"),
 (3, r"\bcash[- ]?flow (?:lending|underwriting|data|based)\b", "Lending decisions using account data"),
 (3, r"\brent (?:payment )?reporting\b|\bboost (?:your |their )?credit scores?\b", "Customers share payment history to improve credit"),
 (3, r"\baccount[- ]to[- ]account\b|\binstant bank payments?\b|\ba2a payments?\b", "Account-to-account payments"),
 (3, r"\b(?:energy|electricity|gas|usage|consumption) data\b", "Customer energy usage data"),
 (3, r"\b(?:export|download|transfer|port|move)(?:s|ing)? (?:your|their) (?:own )?data\b", "Customers move their data between services"),
 (3, r"\b(?:real[- ]time|live) (?:fuel|petrol|diesel|tariff|charging|ev charging) prices?\b|\bprice transparency\b|\b(?:price|pricing|tariff) (?:data|feed|api)\b", "Business price data shared for transparency"),
 (3, r"\b(?:chargepoint|charge point|ev charging) data\b", "Shared EV charging data"),
 (3, r"\bdigital receipts?\b|\bloyalty (?:card )?data\b", "Customer purchase data"),
 (2, r"\bswitch(?:ing)? (?:supplier|provider|tariff|broadband|mobile|energy|bank|account)s?\b", "Easier switching"),
 (2, r"\bdata[- ]sharing\b|\bshared data\b", "Data sharing"),
 (2, r"\baccounting (?:data|software)\b", "Business accounting data shared with lenders/services"),
 (2, r"\bconsent\b", "Consent-based data use"),
 (1, r"\bapis?\b", ""), (1, r"\b(?:fintech|proptech|energytech|insurtech|regtech|agritech)\b", ""),
 (1, r"\b(?:fca|ofgem|ofcom|cma|data \(use and access\) act|duaa)\b", ""),
 (1, r"\b(?:launch(?:es|ed)?|partner(?:s|ship|ed)?|pilot|trial|rolls? out|raises?|funding|series [a-e]|acquires?|goes live|integrat(?:es|ion)|unveils?|selects?|expands?)\b", ""),
]

SECTORS = {
 "Banking (payments)": r"open banking|pay(?:ing)? by bank|payments?|\bbank\b|current account|vrp",
 "Financial services": r"open finance|lend(?:er|ing)|mortgage|credit|pension|insur|savings|wealth|affordability",
 "Road fuels": r"fuel|petrol|diesel|forecourt",
 "Energy": r"energy|electricity|\bgas\b|smart meter|tariff|ofgem|heat pump",
 "Property": r"property|conveyanc|homebuy|home buy|estate agent|land registry|mortgage broker|proptech",
 "Retail": r"retail|loyalty|receipt|grocer|supermarket|shopper",
 "Digital markets": r"data portability|platform|app store|social media|export your data|transfer your data",
 "Transport": r"transport|ev charg|chargepoint|charge point|journey|rail|\bbus\b|mobility",
 "Telecommunications": r"telecom|broadband|mobile (?:phone|network|usage|tariff)|ofcom|one touch switch",
 "Agrifood": r"farm|agri|food supply|traceab",
}

EXCLUDE = r"\bnhs\b|patient|clinical|hospital|health ?(?:records|data|tech)|medtech|\bgp\b|data cent(?:re|er)s?|smart data storage|crypto|bitcoin"
NON_UK = r"\b(?:india|indian|nigeria|kenya|australia|australian|brazil|canada|canadian|us bank|u\.s\.|america|saudi|uae|dubai|singapore|philippines|pakistan|indonesia|mexico|south africa|europe's|eu's)\b"
UK = r"\buk\b|britain|british|england|scotland|wales|northern ireland|london|manchester|belfast|edinburgh|cardiff|birmingham|leeds|bristol|fca|ofgem|ofcom|\bcma\b|£"
KEEP_FROM = 4
