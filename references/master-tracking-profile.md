# MASTER_TRACKING profile

This profile is anchored to `20260924_Master_Tracking_KTNB.xlsx`.

## Physical structure

- Sheet: `MASTER_TRACKING`
- Title rows: 1-2
- Header row: 3
- Data starts: row 4
- Data columns: 32
- Rows: 445
- Stable IDs: 241
- Snapshots: 10/09/2026 and 17/09/2026
- IDs represented in both snapshots: 202

## Canonical columns

`Snapshot`, `ID`, `Source_Sheet`, `Source_Row`, `Snapshot+ID`, `Mức độ tập trung`, `Nhận định và kiến nghị`, `Dấu hiệu`, `STT_RAW`, `VPLĐ_Group`, `Topic_Group`, `KHỐI`, `Tóm tắt nội dung chỉ đạo`, `Chịu trách nhiệm (PIC)`, `Kỳ họp (RAW)`, `Kỳ họp đầu tiên (Date)`, `Kỳ họp mới nhất (Date)`, `Tổng số kỳ họp`, `Thời hạn (RAW)`, `Thời hạn đầu tiên (Date)`, `Thời hạn mới nhất (Date)`, `Số lần thay đổi thời hạn`, `Số ngày còn lại`, `Kết quả/tiến độ đến thời điểm báo cáo`, `Hoàn Thành`, `Thực hiện đúng tiến độ`, `Chưa hoàn thành`, `Dự kiến thời gian hoàn thành (RAW)`, `Dự kiến đầu tiên (Date)`, `Dự kiến mới nhất (Date)`, `Số lần thay đổi dự kiến`, `Chênh lệch dự kiến so với thời hạn (Ngày)`.

## Observed dataset facts

- 166 rows are numerically overdue.
- 184 rows state `Không giao thời hạn`.
- 50 rows have 0-14 days remaining.
- 18 rows are marked complete, 384 marked on track, and 25 marked incomplete after normalizing `X` and `x`.
- 202 IDs have at least two snapshots; 154 have unchanged normalized progress text between the latest two snapshots.
- Common activity-language counts in progress text: `đang phối hợp` 45, `đang trình` 53, `chờ phê duyệt` 6, `dự kiến` 68, `trình lại` 2, `góp ý lần 2` 3, `không thay đổi` 2, `đã nhận chỉ đạo` 1, `thực hiện theo chỉ đạo` 17.

These counts describe this fixture and are not classification thresholds.

## Interpretation priority

1. Stable ID and snapshot history.
2. Directive scope and required outputs.
3. Normalized timing fields.
4. Progress narrative and evidence.
5. Three source status marks.
6. PIC accountability and dependencies.
7. Existing narrative columns as prior analyst work, not unquestioned truth.

## Related sheets

- `Alert_levels`: business definitions for ĐỎ/CAM/VÀNG/XANH/XÁM.
- `Results`: 28 ordered text-interpretation rules.
- `Ly_do`: 11 ordered standardized tracking states.
- `Topics`: business topic taxonomy.
- `Schema`: field-level lineage and normalization rules.
- `QC_Notes`: workbook quality flags and actions.
