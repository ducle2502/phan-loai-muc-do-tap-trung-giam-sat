# phan-loai-muc-do-tap-trung-giam-sat

From the skill directory:

```bash
python scripts/profile_master_tracking.py evals/files/master_tracking_fixture.xlsx --output profile.json
python scripts/prepare_classification.py evals/files/master_tracking_fixture.xlsx --output classification-plan.json
python scripts/validate_classification.py output.csv --report validation.json
python scripts/run_package_checks.py --json-out package-qc.json
```
