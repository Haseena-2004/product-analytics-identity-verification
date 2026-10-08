"""Generates a SIMULATED identity-verification dataset (1,500 records). Not real customer data."""
import csv, random, datetime
random.seed(42)
N = 1500
docs = {"Aadhaar":(.30,.90),"PAN":(.22,.93),"Passport":(.14,.80),"Driving License":(.16,.82),
        "Voter ID":(.10,.74),"National ID (Intl)":(.08,.62)}
channels = {"Android":.55,"iOS":.25,"Web":.20}
chan_mod = {"Android":-.05,"iOS":.02,"Web":-.02}
segments = ["Fintech Lending","Neobank","Crypto Exchange","Gaming & Wallets"]
seg_mod = {"Fintech Lending":0,"Neobank":.02,"Crypto Exchange":-.06,"Gaming & Wallets":-.03}
reasons = ["Blurry Image","Glare/Reflection","Document Expired","Name Mismatch","Face Match Failed",
           "OCR Extraction Error","Liveness Failed","API Timeout","Unsupported Document Format"]
def pick(d): return random.choices(list(d), weights=list(d.values()))[0]
start = datetime.datetime(2026,8,1)
rows = []
for i in range(1, N+1):
    doc = random.choices(list(docs), weights=[v[0] for v in docs.values()])[0]
    ch, seg = pick(channels), random.choice(segments)
    ts = start + datetime.timedelta(seconds=random.randint(0, 30*86400))
    hour = ts.hour
    p = docs[doc][1] + chan_mod[ch] + seg_mod[seg] - (0.05 if 20 <= hour <= 23 else 0)
    ok = random.random() < p
    w = {r:1 for r in reasons}
    if ch == "Android": w["Blurry Image"] += 3
    if doc in ("Voter ID","National ID (Intl)"): w["OCR Extraction Error"] += 5; w["Unsupported Document Format"] += 3
    if doc == "Passport": w["Glare/Reflection"] += 3
    if seg == "Crypto Exchange": w["Liveness Failed"] += 3; w["Face Match Failed"] += 2
    if 20 <= hour <= 23: w["API Timeout"] += 4
    reason = "" if ok else pick(w)
    base = random.lognormvariate(7.6, .35)
    if doc == "National ID (Intl)": base *= 1.6
    if reason == "API Timeout": base = random.uniform(8000, 15000)
    rows.append([f"TXN{i:05d}", ts.strftime("%Y-%m-%d %H:%M:%S"), doc, ch, seg,
                 "SUCCESS" if ok else "FAILED", reason, int(base),
                 random.randint(5,95) if not ok else random.randint(1,60),
                 min(4, int(random.expovariate(1.2)) + (0 if ok else 1))])
with open("data/verification_transactions.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["txn_id","created_at","document_type","channel","client_segment","status",
                "failure_reason","processing_time_ms","risk_score","retry_count"])
    w.writerows(rows)
print("rows:", len(rows))
