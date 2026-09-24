---
name: phan-loai-muc-do-tap-trung-giam-sat
description: Use this skill to assign, review, explain, or validate `Mức độ tập trung` as ĐỎ, CAM, VÀNG, XANH, or XÁM for rows in the KTNB directive-monitoring workbook, especially sheet `MASTER_TRACKING`. Activate for supervisory prioritization, escalation, closure readiness, overdue or at-risk directives, weak evidence, unclear PIC accountability, status conflicts, and reclassification across Snapshot and stable ID. Do not use for employee performance, attitude, intent, or capability assessment.
compatibility: Requires Python 3.9+ and openpyxl for bundled XLSX planning and validation scripts.
metadata:
  author: internal-audit
  version: "4.0"
---

# Objective

Classify the supervisory attention required from Ban Kiểm soát for each directive ID. Classify execution risk and reporting reliability, not topic importance or human performance.

Allowed values: `ĐỎ`, `CAM`, `VÀNG`, `XANH`, `XÁM`.

# Workbook anchor

Default source is `MASTER_TRACKING` in the KTNB workbook. Read row 3 as headers and rows 4 onward as data. Treat:

- `ID` as the stable directive key across snapshots;
- `Snapshot` as assessment date;
- the latest row per `ID` as current state;
- prior rows with the same `ID` as history;
- `Source_Sheet` and `Source_Row` as provenance;
- RAW date fields as provenance and normalized Date fields as calculation inputs;
- `Alert_levels`, `Results`, `Ly_do`, `Schema`, and `QC_Notes` as workbook-controlled reference sheets.

Read `references/master-tracking-profile.md` before classification. Read `references/results-rules.md` when interpreting progress text. Read `references/classification-rules.md` before assigning a final level.

# Workflow

- [ ] Run `python scripts/profile_master_tracking.py <workbook.xlsx> --output profile.json`.
- [ ] Run `python scripts/prepare_classification.py <workbook.xlsx> --output classification-plan.json`.
- [ ] Review every candidate signal against source text and same-ID history.
- [ ] Complete `references/decision-record.md` for each ID.
- [ ] Assign one level with decisive evidence, PIC-control issue, handling, and review gate.
- [ ] Write only to `Mức độ tập trung` if editing the workbook; do not overwrite source, normalized, narrative, or provenance columns.
- [ ] Validate the exported classification CSV with `python scripts/validate_classification.py <output.csv> --report validation.json`.
- [ ] After package changes, run `python scripts/run_package_checks.py`.

# Precedence

Apply in order and stop at the first fully supported level:

1. `XÁM`: minimum facts are insufficient for reliable assessment.
2. `ĐỎ`: serious consequence or failed mandatory readiness is evidenced, and immediate authority intervention is required.
3. `CAM`: significant deviation or credible non-completion risk is evidenced.
4. `VÀNG`: the assignment is assessable, but evidence, closure criteria, progress reliability, dependency, or ownership requires verification.
5. `XANH`: timely execution or complete closure is positively evidenced.

Do not use `XÁM` when available facts already establish `ĐỎ`, `CAM`, or `VÀNG` despite secondary gaps.

# Dataset-specific controls

- Normalize `X` and `x` as marked status values.
- Evaluate `Hoàn Thành`, `Thực hiện đúng tiến độ`, and `Chưa hoàn thành` together. Multiple marks are a data defect, not a risk level.
- Numeric `Số ngày còn lại < 0` means overdue; `0..14` means near due; text `Không giao thời hạn` means no specific deadline.
- `Chênh lệch dự kiến so với thời hạn (Ngày) > 0` means the latest forecast exceeds the deadline.
- Do not accept `Thực hiện đúng tiến độ = X` when timing or narrative evidence contradicts it.
- Do not accept `Hoàn Thành = X` without full scope and evidentiary closure.
- Activity language such as `đang phối hợp`, `đang trình`, `chờ phê duyệt`, `dự kiến`, `trình lại`, `góp ý lần 2`, or `thực hiện theo chỉ đạo` is not output evidence.
- Strong evidence includes issued decisions, signed contracts, acceptance records, quantified results, completion ratios tied to scope, document numbers, approval dates, and actual operating KPIs.
- External dependencies such as HĐTV, Chủ sở hữu, NHNN, HDBank, FinX, Galaxy, or BPMS do not remove the PIC's duty to identify escalation, action, and next commitment.
- Topic names, including Core T24, compliance, liquidity, capital, critical data, or core systems, never establish `ĐỎ` by themselves.
- Reassess every snapshot. Preserve the old level as history; do not blindly carry it forward.

# Human review gates

Set `Cần rà soát thủ công = Có` for:

- every proposed `ĐỎ`;
- every proposed `XANH` closure;
- unresolved adjacent-level boundary;
- contradiction between status marks and narrative/timing;
- unclear or transferred PIC where accountability is material;
- serious consequence inferred from domain context but not explicitly evidenced.

# Output contract

```text
Snapshot | ID | Mức độ tập trung | Căn cứ phân loại | Dấu hiệu quyết định | Nhận biết về trách nhiệm | Cách xử lý | Cần rà soát thủ công | Lý do rà soát
```

Preserve `Source_Sheet`, `Source_Row`, and the original workbook fields in any detailed export.

# Final checklist

- [ ] Latest snapshot and full same-ID history reviewed.
- [ ] Exactly one allowed level selected.
- [ ] Classification uses workbook fields and evidence, not topic labels alone.
- [ ] `ĐỎ` has severity/mandatory failure plus immediate authority need.
- [ ] Overdue alone is not `ĐỎ`.
- [ ] `XANH` has positive evidence.
- [ ] `XÁM` means inability to classify, not low risk.
- [ ] PIC comments are limited to accountability controls.
- [ ] Handling matches the level.
- [ ] Human review gates are applied.
