# API Performance & Service Benchmarking
**Tools:** SQL, Excel, Power BI | **Data:** 24 simulated API services (+ 14-day p95 latency series, competitor benchmark)

## Business questions
1. Which services are underperforming on latency, success rate or coverage?
2. Where do we lag the competitor benchmark?
3. Which issues hurt the most requests per month (impact-based priority)?

## Metrics tracked (5 core)
p95 latency, success rate, error/timeout rate, request volume, coverage % (plus competitor p95 and success).

## Key findings (seeded run; verify against your output)
- **Passport Verification** (~58% slower p95 than competitor) and **Intl ID OCR** (~48% slower, ~4pt lower success) are the biggest gaps.
- **Voter ID OCR** and **Driving License Verification** have the lowest success rates (~91-92%).
- Latency spikes on specific days for Intl ID OCR, Passport/Voter ID Verification and Face Match (see `04_latency_spike_days`).
- Coverage below 90% on Intl ID OCR, Passport Verification and Address Match.

## Recommendations
1. Add caching / timeout + fallback source for slow government verification APIs.
2. Retrain / expand templates for Voter ID and Intl ID OCR to close the success gap.
3. Set SLO alerts (p95 > 1.8x rolling average) to catch spikes within a day.
4. Prioritise fixes by `est_failed_requests_per_month`, not by percentage alone.

## Excel tracker
Open `outputs/01_service_scorecard.csv` in Excel; apply conditional formatting on `health` (RED/AMBER/GREEN) and add a chart of p95 vs competitor p95. Save as `benchmark_tracker.xlsx`.
