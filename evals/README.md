# Evaluation runbook

Use clean, isolated sessions. Do not reuse development conversation context.

For every case in `evals.json`:

1. Run once with this skill loaded.
2. Run the same prompt without the skill, or against the prior accepted skill version.
3. Save outputs separately under an external workspace:

```text
workspace/
  history.json
  iteration-N/
    eval-<id>/
      with_skill/outputs/
      with_skill/grading.json
      with_skill/timing.json
      baseline/outputs/
      baseline/grading.json
      baseline/timing.json
    benchmark.json
```

Grade every statement in `expectations`. Record evidence for each pass or failure. Compare quality, false escalation, false de-escalation, unsupported classifications, token use, and runtime. Do not put fabricated pass rates in this package.

The benchmark and version history belong in the external evaluation workspace, not in the distributed skill directory.
