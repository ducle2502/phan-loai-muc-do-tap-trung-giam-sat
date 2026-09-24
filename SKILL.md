---
name: phan-loai-muc-do-tap-trung-giam-sat
description: Use this skill when the user wants to assign, review, explain, or validate `Mức độ tập trung` as ĐỎ, CAM, VÀNG, XANH, or XÁM for directive, project, audit, or management-tracking rows. Activate for supervisory prioritization, escalation, closure readiness, overdue or at-risk work, weak evidence, unclear PIC accountability, conflicting status, or reclassification across snapshots. Do not use for employee performance, attitude, intent, or capability assessment.
compatibility: Requires Python 3.9+ for bundled CSV planning and validation scripts.
metadata:
  author: internal-audit
  version: "2.0"
---

# Objective

Classify the attention required from the Board of Supervisors. Do not classify inherent topic importance or human performance.

Allowed values only: `ĐỎ`, `CAM`, `VÀNG`, `XANH`, `XÁM`.

# Workflow

- [ ] Run `python scripts/prepare_classification.py <input.csv> --output classification-plan.json` for batch work.
- [ ] Review the latest snapshot and all history for each ID. Script signals are candidates, not decisions.
- [ ] Read `references/classification-rules.md` and complete `references/decision-record.md`.
- [ ] Assign one level and state decisive evidence, PIC-control issue, handling, and review gate.
- [ ] Run `python scripts/validate_classification.py <output.csv> --report validation.json`.
- [ ] Fix all errors and rerun. Deliver only after `status` is `pass`.
- [ ] After changing this package, run `python scripts/run_package_checks.py`.

For a single row in chat, use the same reasoning without scripts.

# Precedence

Apply in order and stop at the first fully supported level:

1. `XÁM`: minimum facts are insufficient for reliable assessment.
2. `ĐỎ`: serious consequence or failed mandatory readiness is evidenced, and immediate authority intervention is required.
3. `CAM`: significant deviation or credible non-completion risk is evidenced.
4. `VÀNG`: assignment is assessable, but evidence, closure criteria, progress reliability, dependency, or ownership still requires verification.
5. `XANH`: timely execution or complete closure is positively evidenced.

Do not use `XÁM` when available facts already establish `ĐỎ`, `CAM`, or `VÀNG` despite secondary gaps.

# Non-negotiable rules

- Never classify from one keyword, topic name, `VPLĐ_Group`, or `Topic_Group` alone.
- Overdue alone normally supports `CAM`, not automatically `ĐỎ`.
- Core Banking, compliance, legal, liquidity, capital, or data topics are not automatically `ĐỎ`.
- Missing deadline alone is not automatically `XÁM` when the assignment remains assessable.
- `XANH` requires positive evidence; absence of warning signs is insufficient.
- `Hoàn Thành = X` cannot override incomplete scope, missing evidence, pending approval, or material work still underway.
- `XÁM` means unclassifiable, not safe, complete, controlled, or low priority.
- PIC analysis is limited to role clarity, authority, final accountability, handover, dependency removal, and response.
- Reassess each snapshot. A changing overdue-day count alone does not necessarily move `CAM` to `ĐỎ`.
- Human approval is mandatory for every `ĐỎ`, proposed closure under `XANH`, and unresolved adjacent-level boundary.

# Decision record

Complete these fields before the final level:

```text
minimum_facts_sufficient
evidenced_serious_consequence
mandatory_condition_failed
immediate_authority_intervention_required
significant_deviation_or_delay_risk
verification_gap_only
positive_green_evidence
pic_control_issue
selected_level
boundary_considered
decisive_evidence
human_review_required
```

# Available scripts

- `scripts/prepare_classification.py`: builds a per-ID JSON plan.
- `scripts/validate_classification.py`: checks final CSV logic and review gates.
- `scripts/run_package_checks.py`: checks package structure, eval schemas, trigger coverage, scripts, and fixtures.

# Output contract

```text
Snapshot | ID | Mức độ tập trung | Căn cứ phân loại | Dấu hiệu quyết định | Nhận biết về trách nhiệm | Cách xử lý | Cần rà soát thủ công | Lý do rà soát
```

Preserve source rows and evidence provenance.

# Final checklist

- [ ] One allowed level assigned.
- [ ] Latest snapshot assessed and history reviewed.
- [ ] Precedence and border rule applied.
- [ ] Decisive source-bound evidence stated.
- [ ] Overdue not converted automatically to `ĐỎ`.
- [ ] `XANH` supported by positive evidence.
- [ ] `XÁM` used only for genuine inability to classify.
- [ ] PIC text contains no human performance assessment.
- [ ] Handling matches the level.
- [ ] Required human-review gates applied.
