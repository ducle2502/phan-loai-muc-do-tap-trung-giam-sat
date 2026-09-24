---
name: phan-loai-muc-do-tap-trung-giam-sat
description: Use this skill to assign, review, explain, or validate `Mức độ tập trung` as ĐỎ, CAM, VÀNG, XANH, or XÁM for rows in the KTNB directive-monitoring workbook, especially `MASTER_TRACKING`. Activate for supervisory prioritization, escalation, closure readiness, overdue or at-risk directives, weak evidence, unclear PIC accountability, status conflicts, reclassification across Snapshot and stable ID, and whenever an upstream `danh-gia-rui-ro` result is available. Link economic consequence and probability from `danh-gia-rui-ro` by exact `Snapshot+ID`, but never convert severity mechanically into a supervision level. Do not use for employee performance, attitude, intent, or capability assessment.
compatibility: Requires Python 3.9+ and openpyxl for XLSX planning; bundled CSV linkage and validation scripts use the Python standard library.
metadata:
  author: internal-audit
  version: 5.0
---

# Objective

Classify the supervisory attention required from Ban Kiểm soát for each directive ID. Classify execution risk, economic exposure, urgency, and reporting reliability, not topic importance or human performance.

Allowed values: `ĐỎ`, `CAM`, `VÀNG`, `XANH`, `XÁM`.

## Workbook anchor

Default source is `MASTER_TRACKING` in the KTNB workbook. Read row 3 as headers and rows 4 onward as data.

Treat:

- `ID` as the stable directive key across snapshots.
- `Snapshot` as assessment date.
- `Snapshot+ID` as the exact point-in-time integration key.
- The latest row per `ID` as current state; prior rows with the same `ID` as history.
- `Source_Sheet` and `Source_Row` as provenance.
- RAW date fields as provenance and normalized Date fields as calculation inputs.
- `Alert_levels`, `Results`, `Ly_do`, `Schema`, and `QC_Notes` as workbook-controlled references.

Read the package's existing profile, result, and classification references before assigning a level. Read `references/risk-integration-contract.md` whenever a `danh-gia-rui-ro` output is present.

# Linked workflow

1. Profile the source workbook and prepare the normal classification plan using the package's existing scripts.
2. Obtain the upstream `danh-gia-rui-ro` result with exactly these columns:
   - `Snapshot+ID`
   - `Mức độ nghiêm trọng của hậu quả (tiền, thời gian, con người) và khả năng sinh ra rủi ro`
3. Run:

```bash
python scripts/link_risk_results.py classification-input.csv risk-output.csv --output linked-input.csv --report risk-link-report.json
```

4. Review every linked risk result against:
   - source narrative;
   - timing and status marks;
   - same-ID history;
   - evidence supporting the monetary estimate;
   - the need for immediate authority intervention.
5. Complete the existing decision record for each ID and add the linked-risk fields defined in `references/risk-integration-contract.md`.
6. Assign one level with decisive evidence, economic consequence, probability, PIC-control issue, handling, and review gate.
7. Write only to `Mức độ tập trung` if editing the workbook. Do not overwrite source, normalized, narrative, provenance, or upstream risk columns.
8. Validate the classification with the package's existing validator, then run:

```bash
python scripts/validate_risk_linkage.py linked-output.csv --report risk-link-qc.json
```

# Precedence

Apply in order and stop at the first fully supported level:

1. `XÁM`: minimum facts are insufficient for reliable assessment.
2. `ĐỎ`: serious economic consequence or failed mandatory readiness is evidenced, and immediate authority intervention is required.
3. `CAM`: significant economic exposure, material deviation, or credible non-completion risk is evidenced, but immediate authority intervention is not yet the only reasonable response.
4. `VÀNG`: the assignment is assessable, but evidence, closure criteria, estimate quality, dependency, progress reliability, or ownership requires verification.
5. `XANH`: timely execution or complete closure is positively evidenced, including evidence that the economic exposure has been removed or accepted by competent authority.

Do not use `XÁM` when available facts already establish `ĐỎ`, `CAM`, or `VÀNG` despite secondary gaps.

# Using `danh-gia-rui-ro` without mechanical mapping

The upstream result provides two inputs:

- severity of economic consequence: `Rất nghiêm trọng`, `Nghiêm trọng`, `Trung bình`, `Nhẹ`, or `Không ảnh hưởng`;
- probability: `90%`, `75%`, `50%`, `25%`, or `10%`, with evidence.

These inputs strengthen classification, but they do not decide it alone.

## Strong support for ĐỎ

A proposed `ĐỎ` normally requires all three:

1. Economic consequence is `Rất nghiêm trọng`, or a mandatory legal/operational readiness failure can stop a material money-making activity.
2. Probability is at least 75%, or the loss/blockage has already begun.
3. Immediate intervention by HĐTV, Chủ sở hữu, TGĐ, BKS, or competent authority is necessary to prevent or contain the consequence.

A `Rất nghiêm trọng + 50%` scenario is not automatically ĐỎ. It is usually CAM or VÀNG unless an irreversible decision window or mandatory intervention makes delay unacceptable.

## Strong support for CAM

Use CAM when one of these is supported:

- `Rất nghiêm trọng` consequence at 50% with credible evidence and a live decision/dependency.
- `Nghiêm trọng` consequence at 75% or 90% with material delay, weak controls, or no dated recovery plan.
- A lower monetary consequence threatens repeated non-completion across multiple snapshots or materially weakens owner economics.

## Strong support for VÀNG

Use VÀNG when:

- the economic estimate is screening-only and underlying transaction value is missing;
- the consequence is `Trung bình` or lower but evidence, closure, dependency, or ownership needs verification;
- the severity/probability labels conflict with source facts;
- an upstream risk result is present but cannot be traced to a calculation or source value.

## Conditions for XANH

Do not assign XANH merely because the row says completed/on track. Require evidence of scope completion and, where upstream risk was material, evidence that:

- the money-making activity is operating;
- the blocked capital or source of loss has been released;
- the legal/operational restriction is removed;
- the owner-level exposure is accepted by competent authority; or
- a subsequent `danh-gia-rui-ro` result shows the consequence reduced to `Nhẹ`/`Không ảnh hưởng` with support.

# Dataset-specific controls

- Normalize `X` and `x` as marked status values.
- Evaluate `Hoàn Thành`, `Thực hiện đúng tiến độ`, and `Chưa hoàn thành` together. Multiple marks are a data defect, not a risk level.
- `Số ngày còn lại < 0` means overdue; `0..14` means near due; `Không giao thời hạn` means no specific deadline.
- `Chênh lệch dự kiến so với thời hạn (Ngày) > 0` means the latest forecast exceeds the deadline.
- Do not accept `Thực hiện đúng tiến độ = X` when timing, narrative, or linked risk evidence contradicts it.
- Do not accept `Hoàn Thành = X` without full scope, evidentiary closure, and treatment of residual economic exposure.
- Activity language such as `đang phối hợp`, `đang trình`, `chờ phê duyệt`, `dự kiến`, `trình lại`, `góp ý lần 2`, or `thực hiện theo chỉ đạo` is not output evidence.
- Strong evidence includes issued decisions, signed contracts, acceptance records, quantified results, completion ratios tied to scope, document numbers, approval dates, actual operating KPIs, transaction values, released capital, realized income, or verified recovery amounts.
- External dependencies do not remove the PIC's duty to identify escalation, action, economic impact, and next commitment.
- Topic names never establish `ĐỎ` by themselves.
- Reassess every snapshot. Preserve the old level as history; do not blindly carry it forward.
- Link only by exact `Snapshot+ID`. Never join upstream risk by `ID` alone because that can attach a prior snapshot's exposure to the current state.

# Human review gates

Set `Cần rà soát thủ công = Có` for:

- every proposed `ĐỎ`;
- every proposed `XANH` closure;
- `Rất nghiêm trọng` economic consequence at any probability;
- all screening estimates of 100 tỷ đồng or more without a source transaction value;
- unresolved adjacent-level boundary;
- contradiction between upstream risk, status marks, narrative, or timing;
- unclear/transferred PIC where accountability is material;
- missing or duplicate `Snapshot+ID` linkage;
- serious consequence inferred from domain context but not explicitly evidenced.

# Output contract

```text
Snapshot | ID | Snapshot+ID | Mức độ tập trung | Căn cứ phân loại | Dấu hiệu quyết định | Mức hậu quả kinh tế | Giá trị kinh tế phơi nhiễm | Khả năng xảy ra (%) | Căn cứ xác suất | Nhận biết về trách nhiệm | Cách xử lý | Cần rà soát thủ công | Lý do rà soát
```

Preserve `Source_Sheet`, `Source_Row`, upstream risk text, and original workbook fields in detailed exports.

# Final checklist

- Latest snapshot and full same-ID history reviewed.
- Exact `Snapshot+ID` risk link checked.
- Exactly one allowed level selected.
- Classification uses evidence, not topic labels or severity labels alone.
- `ĐỎ` has serious consequence, high/immediate likelihood, and immediate authority need.
- Overdue alone is not `ĐỎ`.
- `XANH` has positive closure and exposure-removal evidence.
- `XÁM` means inability to classify, not low risk.
- Risk estimate is identified as direct, calculated, or screening-only.
- PIC comments are limited to accountability controls, not personal performance.
- Handling matches the level and the owner's economic interest.
