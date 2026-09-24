# Grading rubric

## Hard failures

Any hard failure makes the case fail:

- uses a level outside ĐỎ, CAM, VÀNG, XANH, XÁM;
- assigns ĐỎ from topic name or overdue alone;
- assigns XANH without positive evidence;
- treats XÁM as low risk or controlled;
- omits required human review for ĐỎ or proposed XANH closure;
- evaluates employee competence, attitude, intent, or performance;
- loses stable ID, Snapshot, Source_Sheet, or Source_Row traceability.

## Expectation grading

For each expectation use:

```json
{
  "expectation": "verifiable statement",
  "passed": true,
  "evidence": "exact output passage or generated artifact field"
}
```

## Comparison decision

- `won`: higher expectation pass rate with no new hard failure.
- `lost`: lower pass rate or any new hard failure.
- `tie`: equal pass rate and no material quality difference.

Do not use style preference alone to declare a winner.
