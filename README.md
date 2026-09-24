# phan-loai-muc-do-tap-trung-giam-sat

```bash
python scripts/prepare_classification.py input.csv --output classification-plan.json
python scripts/validate_classification.py output.csv --report validation.json
python scripts/run_package_checks.py
```

V2 adds a structured decision record, expectation-based evals, positive and near-miss trigger evals, version history, and deterministic package checks. External with-skill versus baseline agent runs are still required before recording pass rates.
