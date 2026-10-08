"""Generates a SIMULATED OCR training-data sourcing & tagging tracker."""
import csv, random
random.seed(11)
docs = [("Aadhaar","IN","Identity"),("PAN","IN","Identity"),("Passport","IN","Identity"),("Driving License","IN","Identity"),
 ("Voter ID","IN","Identity"),("Bank Statement","IN","Financial"),("Utility Bill","IN","Address Proof"),
 ("GST Certificate","IN","Business"),("Passport","ID","Identity"),("National ID","ID","Identity"),
 ("National ID","PH","Identity"),("Driver License","PH","Identity"),("National ID","NG","Identity"),
 ("Passport","NG","Identity"),("National ID","VN","Identity"),("Driver License","MX","Identity")]
with open("data/ocr_dataset_tracker.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["doc_type","country","category","target_samples","sourced_samples","tagged_samples","qa_passed_samples",
                "blurry_pct","low_light_pct","priority","source_channel"])
    for dt, c, cat in docs:
        t = 5000 if c == "IN" else 2000
        s = int(t*random.uniform(.85,1.05)) if c == "IN" else int(t*random.uniform(.15,.7))
        tg = int(s*random.uniform(.6,.95)); qa = int(tg*random.uniform(.85,.97))
        w.writerow([dt,c,cat,t,s,tg,qa,round(random.uniform(3,18),1),round(random.uniform(2,12),1),
                    "High" if c!="IN" or dt in("Voter ID","Passport") else "Medium",
                    random.choice(["Customer consented","Partner vendor","Synthetic augmentation","Internal capture"])])
