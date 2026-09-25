# Python Data Pipeline & ETL

A modular ETL pipeline that extracts CSV sales data, validates records, transforms business metrics, and writes analytics-ready output.

## Pipeline
Extract -> Validate -> Transform -> Load

## Features
- Type-safe data models
- Validation and rejected-row reporting
- Aggregation by category/month
- Idempotent output generation
- CLI entry point
- Unit-testable transformation layer

Run:
```bash
pip install -r requirements.txt
python pipeline.py
```
