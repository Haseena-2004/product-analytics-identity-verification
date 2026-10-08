"""Generates SIMULATED API service metrics for 24 services + 14-day latency series + competitor benchmark."""
import csv, random
random.seed(7)
services = [("Aadhaar OCR","OCR"),("PAN OCR","OCR"),("Passport OCR","OCR"),("Driving License OCR","OCR"),
 ("Voter ID OCR","OCR"),("Intl ID OCR","OCR"),("Face Match","Biometrics"),("Liveness Check","Biometrics"),
 ("PAN Verification","Govt Verification"),("Aadhaar Offline eKYC","Govt Verification"),
 ("Driving License Verification","Govt Verification"),("Voter ID Verification","Govt Verification"),
 ("Passport Verification","Govt Verification"),("Email Risk","Fraud Signals"),("Phone Risk","Fraud Signals"),
 ("Device Intelligence","Fraud Signals"),("IP Risk","Fraud Signals"),("Name Match","Data Matching"),
 ("Address Match","Data Matching"),("Bank Account Verification","Financial"),("UPI Verification","Financial"),
 ("GST Verification","Business"),("Company (MCA) Lookup","Business"),("AML Screening","Compliance")]
bad_latency = {"Voter ID Verification","Passport Verification","Intl ID OCR"}
low_success = {"Voter ID OCR","Intl ID OCR","Driving License Verification"}
low_cov = {"Intl ID OCR","Address Match","Passport Verification"}
with open("data/api_service_metrics.csv","w",newline="") as f, open("data/api_daily_latency.csv","w",newline="") as g:
    w, d = csv.writer(f), csv.writer(g)
    w.writerow(["service","category","p50_ms","p95_ms","success_rate_pct","error_rate_pct","timeout_rate_pct",
                "monthly_requests","coverage_pct","competitor_p95_ms","competitor_success_pct","missing_fields_pct"])
    d.writerow(["service","day","p95_ms"])
    for name, cat in services:
        p50 = random.randint(180, 900) * (3 if name in bad_latency else 1)
        p95 = int(p50 * random.uniform(1.8, 2.6))
        succ = round(random.uniform(97.5, 99.7) - (random.uniform(4, 9) if name in low_success else 0), 2)
        tout = round(random.uniform(.1, .6) + (1.2 if name in bad_latency else 0), 2)
        err = round(100 - succ - random.uniform(0, .3) + 0, 2); err = max(round(100-succ,2)-0.0, 0)
        cov = round(random.uniform(94, 100) - (random.uniform(12, 25) if name in low_cov else 0), 1)
        comp_p95 = int(p95 * random.uniform(.55, 1.15)) if name in bad_latency else int(p95*random.uniform(.9,1.2))
        comp_s = round(succ + random.uniform(-.5, 1.8) + (random.uniform(3,6) if name in low_success else 0), 2)
        w.writerow([name,cat,p50,p95,succ,err,tout,random.randint(20000,4000000),cov,comp_p95,min(comp_s,99.9),
                    round(random.uniform(0,6),1) if cat=="Govt Verification" else round(random.uniform(0,2),1)])
        for day in range(1,15):
            spike = 2.4 if (name in bad_latency and day in (6,7,11)) or (name=="Face Match" and day==9) else 1
            d.writerow([name, f"2026-09-{day:02d}", int(p95*random.uniform(.9,1.1)*spike)])
print("services:", len(services))
