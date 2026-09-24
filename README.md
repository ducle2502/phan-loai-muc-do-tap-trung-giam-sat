# phan-loai-muc-do-tap-trung-giam-sat v4

This skill is anchored to `MASTER_TRACKING` in the included workbook fixture.

From the skill directory:

```bash
python scripts/profile_master_tracking.py evals/files/master_tracking_fixture.xlsx --output profile.json
python scripts/prepare_classification.py evals/files/master_tracking_fixture.xlsx --output classification-plan.json
python scripts/validate_classification.py output.csv --report validation.json
python scripts/run_package_checks.py --json-out package-qc.json
```

Deterministic package QC is included. Comparative quality claims require isolated with-skill and baseline agent runs following `evals/README.md`.
