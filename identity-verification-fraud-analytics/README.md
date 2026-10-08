# Identity Verification & Fraud Analytics
**Tools:** SQL (SQLite dialect), Power BI, Excel | **Data:** 1,500 simulated verification transactions

## Business questions
1. Why do verifications fail, and which failures are fixable by product changes?
2. Which document x channel combinations convert worst?
3. Which client segments need targeted optimisation?
4. Are there time-of-day reliability issues?

## Dataset (`data/verification_transactions.csv`)
`txn_id, created_at, document_type, channel, client_segment, status, failure_reason, processing_time_ms, risk_score, retry_count`

## Key findings (from the seeded run; re-check against your own output)
- Overall success rate ~79.6%; **National ID (Intl) is lowest (~56%)** and ~1.6x slower than other documents.
- **Blurry Image is the #1 failure reason (~20%)**, concentrated on **Android**; OCR errors and unsupported formats dominate Voter ID / Intl ID.
- **Crypto Exchange** has the lowest conversion (~77%), driven by liveness/face-match failures.
- **Evening hours (20-23h)** show more API timeouts (avg ~11.5s on timeout failures).

## Recommendations
1. Add real-time capture guidance (blur/glare detection, auto-capture) in the Android SDK.
2. Prioritise OCR model improvement and template coverage for Voter ID and international IDs.
3. Introduce liveness retry UX and threshold tuning for high-risk segments such as crypto.
4. Investigate evening-peak capacity / timeout handling and add a fallback or retry policy.

## Power BI dashboard (build steps)
1. Get Data > Text/CSV: load `data/verification_transactions.csv` (or files in `outputs/`).
2. Measures (DAX):
   - `Success Rate = DIVIDE(CALCULATE(COUNTROWS(T), T[status]="SUCCESS"), COUNTROWS(T))`
   - `Avg Processing (ms) = AVERAGE(T[processing_time_ms])`
   - `Avg Retries = AVERAGE(T[retry_count])`
   - `High-Risk Failures = CALCULATE(COUNTROWS(T), T[status]="FAILED", T[risk_score]>=75)`
3. Visuals: KPI cards (5), bar chart of failure reasons, matrix (channel x document, failure rate heat-map), line chart of weekly trend, hourly column chart; slicers for segment/channel/document.
4. Export screenshots to `/dashboard` and add them here.

## Run
```bash
python3 generate_data.py
cd .. && python3 run_sql.py p1-identity-verification-fraud-analytics
```
