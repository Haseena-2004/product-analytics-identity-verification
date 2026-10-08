-- name: 01_volume_gap_vs_target
SELECT doc_type, country, target_samples, sourced_samples, target_samples-sourced_samples AS gap,
       ROUND(100.0*sourced_samples/target_samples,1) AS pct_of_target
FROM ocr_dataset_tracker ORDER BY pct_of_target;
-- name: 02_tagging_pipeline_funnel
SELECT doc_type, country, sourced_samples, tagged_samples, qa_passed_samples,
       ROUND(100.0*tagged_samples/sourced_samples,1) AS tagged_pct,
       ROUND(100.0*qa_passed_samples/tagged_samples,1) AS qa_pass_pct
FROM ocr_dataset_tracker ORDER BY tagged_pct;
-- name: 03_quality_risk_images
SELECT doc_type, country, blurry_pct, low_light_pct, ROUND(blurry_pct+low_light_pct,1) AS poor_quality_pct
FROM ocr_dataset_tracker WHERE blurry_pct+low_light_pct > 18 ORDER BY poor_quality_pct DESC;
-- name: 04_country_readiness
SELECT country, SUM(target_samples) AS target, SUM(qa_passed_samples) AS ready_for_training,
       ROUND(100.0*SUM(qa_passed_samples)/SUM(target_samples),1) AS readiness_pct
FROM ocr_dataset_tracker GROUP BY country ORDER BY readiness_pct;
-- name: 05_sourcing_channel_mix
SELECT source_channel, COUNT(*) AS doc_sets, SUM(sourced_samples) AS samples,
       ROUND(AVG(100.0*qa_passed_samples/sourced_samples),1) AS avg_qa_yield_pct
FROM ocr_dataset_tracker GROUP BY source_channel ORDER BY avg_qa_yield_pct DESC;
