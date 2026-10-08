-- name: 01_service_scorecard
SELECT service, category, p95_ms, success_rate_pct, error_rate_pct, coverage_pct,
  CASE WHEN success_rate_pct < 96 OR p95_ms > 2500 OR coverage_pct < 90 THEN 'RED'
       WHEN success_rate_pct < 98.5 OR p95_ms > 1500 THEN 'AMBER' ELSE 'GREEN' END AS health
FROM api_service_metrics ORDER BY CASE WHEN success_rate_pct < 96 OR p95_ms > 2500 OR coverage_pct < 90 THEN 1 WHEN success_rate_pct < 98.5 OR p95_ms > 1500 THEN 2 ELSE 3 END, p95_ms DESC;
-- name: 02_vs_competitor_gaps
SELECT service, p95_ms, competitor_p95_ms,
       ROUND(100.0*(p95_ms-competitor_p95_ms)/competitor_p95_ms,1) AS latency_gap_pct,
       success_rate_pct, competitor_success_pct,
       ROUND(success_rate_pct-competitor_success_pct,2) AS success_gap_pts
FROM api_service_metrics
WHERE p95_ms > competitor_p95_ms*1.1 OR success_rate_pct < competitor_success_pct-1
ORDER BY latency_gap_pct DESC;
-- name: 03_category_summary
SELECT category, COUNT(*) AS services, ROUND(AVG(p95_ms),0) AS avg_p95_ms,
       ROUND(AVG(success_rate_pct),2) AS avg_success_pct, ROUND(AVG(coverage_pct),1) AS avg_coverage_pct
FROM api_service_metrics GROUP BY category ORDER BY avg_p95_ms DESC;
-- name: 04_latency_spike_days
SELECT d.service, d.day, d.p95_ms, ROUND(a.avg_p95,0) AS service_avg_p95
FROM api_daily_latency d
JOIN (SELECT service, AVG(p95_ms) AS avg_p95 FROM api_daily_latency GROUP BY service) a USING(service)
WHERE d.p95_ms > 1.8*a.avg_p95 ORDER BY d.service, d.day;
-- name: 05_coverage_gaps
SELECT service, coverage_pct, monthly_requests FROM api_service_metrics WHERE coverage_pct < 90 ORDER BY coverage_pct;
-- name: 06_impact_prioritisation
SELECT service, monthly_requests, ROUND(100-success_rate_pct,2) AS failure_pct,
       CAST(monthly_requests*(100-success_rate_pct)/100 AS INTEGER) AS est_failed_requests_per_month
FROM api_service_metrics ORDER BY est_failed_requests_per_month DESC LIMIT 10;
-- name: 07_data_quality_checks
SELECT service, missing_fields_pct, timeout_rate_pct FROM api_service_metrics
WHERE missing_fields_pct > 3 OR timeout_rate_pct > 1 ORDER BY missing_fields_pct DESC;
