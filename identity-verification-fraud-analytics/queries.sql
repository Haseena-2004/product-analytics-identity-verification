-- name: 01_overall_kpis
SELECT COUNT(*) AS total_txns,
       ROUND(100.0*SUM(status='SUCCESS')/COUNT(*),2) AS success_rate_pct,
       ROUND(AVG(processing_time_ms),0) AS avg_processing_ms,
       ROUND(AVG(retry_count),2) AS avg_retries,
       ROUND(AVG(risk_score),1) AS avg_risk_score
FROM verification_transactions;
-- name: 02_success_rate_by_document
SELECT document_type, COUNT(*) AS txns,
       ROUND(100.0*SUM(status='SUCCESS')/COUNT(*),2) AS success_rate_pct,
       ROUND(AVG(processing_time_ms),0) AS avg_ms
FROM verification_transactions GROUP BY document_type ORDER BY success_rate_pct;
-- name: 03_failure_reason_breakdown
SELECT failure_reason, COUNT(*) AS failures,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM verification_transactions WHERE status='FAILED'),2) AS pct_of_failures
FROM verification_transactions WHERE status='FAILED' GROUP BY failure_reason ORDER BY failures DESC;
-- name: 04_channel_x_document_failure_hotspots
SELECT channel, document_type, COUNT(*) AS txns,
       ROUND(100.0*SUM(status='FAILED')/COUNT(*),2) AS failure_rate_pct
FROM verification_transactions GROUP BY channel, document_type HAVING txns >= 30
ORDER BY failure_rate_pct DESC LIMIT 10;
-- name: 05_segment_conversion
SELECT client_segment, COUNT(*) AS txns,
       ROUND(100.0*SUM(status='SUCCESS')/COUNT(*),2) AS success_rate_pct,
       ROUND(AVG(retry_count),2) AS avg_retries
FROM verification_transactions GROUP BY client_segment ORDER BY success_rate_pct;
-- name: 06_hourly_success_and_latency
SELECT CAST(strftime('%H', created_at) AS INTEGER) AS hour_of_day, COUNT(*) AS txns,
       ROUND(100.0*SUM(status='SUCCESS')/COUNT(*),2) AS success_rate_pct,
       ROUND(AVG(processing_time_ms),0) AS avg_ms
FROM verification_transactions GROUP BY hour_of_day ORDER BY hour_of_day;
-- name: 07_timeouts_vs_slow_txns
SELECT failure_reason, ROUND(AVG(processing_time_ms),0) AS avg_ms, MAX(processing_time_ms) AS max_ms, COUNT(*) AS n
FROM verification_transactions WHERE status='FAILED' GROUP BY failure_reason ORDER BY avg_ms DESC;
-- name: 08_high_risk_failures
SELECT document_type, COUNT(*) AS high_risk_failed
FROM verification_transactions WHERE status='FAILED' AND risk_score >= 75
GROUP BY document_type ORDER BY high_risk_failed DESC;
-- name: 09_weekly_trend
SELECT strftime('%Y-W%W', created_at) AS week, COUNT(*) AS txns,
       ROUND(100.0*SUM(status='SUCCESS')/COUNT(*),2) AS success_rate_pct
FROM verification_transactions GROUP BY week ORDER BY week;
