# OCR Data Sourcing & Tagging Tracker
**Tools:** SQL, Excel/Python | **Data:** 16 simulated document-type/country datasets

Mirrors the "data sourcing engine for OCR models" responsibility: track volume vs target, tagging progress, QA yield and image quality for each document type.

## Questions answered
- Which document types are furthest from target volume?
- Where is the tagging pipeline bottlenecked?
- Which sources give the best QA yield?
- Which countries are training-ready?

## Findings (seeded run)
International document types (MX, ID, NG) are at 10-30% of target, while India is ~63% training-ready. Prioritise sourcing for those and shift spend toward the highest QA-yield channel (`05_sourcing_channel_mix`).

## Process documented
1. Define target volume per doc type (5,000 for core, 2,000 for new markets).
2. Source via consented customer data, partners, internal capture, synthetic augmentation.
3. Tag fields (name, ID number, DOB, etc.), then QA sample-check; track blur/low-light share.
4. Report gaps weekly using the SQL queries.
