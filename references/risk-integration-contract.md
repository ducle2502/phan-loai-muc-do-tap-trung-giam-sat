# Integration contract with `danh-gia-rui-ro`

## Purpose

Use the risk skill's output as point-in-time economic evidence for supervisory concentration. The risk skill answers “what owner value may be lost and how likely is it?” The concentration skill answers “how much supervisory attention is required now?”

## Required upstream columns

1. `Snapshot+ID`
2. `Mức độ nghiêm trọng của hậu quả (tiền, thời gian, con người) và khả năng sinh ra rủi ro`

The narrative must contain exactly two labeled lines:

- `Hậu quả – [level]: ... [amount with unit] ...`
- `Khả năng xảy ra – [percentage]: ... evidence ...`

## Parsed linked fields

- `Risk_Link_Status`: MATCHED, MISSING, DUPLICATE, or INVALID_FORMAT.
- `Mức hậu quả kinh tế`: Rất nghiêm trọng, Nghiêm trọng, Trung bình, Nhẹ, Không ảnh hưởng.
- `Giá trị kinh tế phơi nhiễm`: preserved text such as `10–100 tỷ đồng`.
- `Khả năng xảy ra (%)`: 90, 75, 50, 25, or 10.
- `Căn cứ xác suất`: evidence text after the percentage.
- `Risk_Estimate_Type`: DIRECT, CALCULATED, or SCREENING.
- `Risk_Source_Text`: complete original upstream value.

## Linkage rules

- Join by exact `Snapshot+ID` only.
- Reject blank or duplicate upstream keys.
- Do not silently select one duplicate.
- Do not carry a prior snapshot's risk result forward.
- Missing linkage does not automatically mean XÁM if the source row independently contains enough facts; it does require manual review when the workflow expects upstream risk.

## Decision relationship

Risk severity and probability are evidence, not a direct color map.

- ĐỎ needs economic materiality plus immediacy and authority intervention.
- CAM captures material exposure or credible non-completion where escalation is strong but not emergency-only.
- VÀNG captures verification needs, estimate uncertainty, or control weakness.
- XANH requires evidence the economic exposure is removed, not merely that paperwork is completed.
- XÁM is reserved for insufficient minimum facts.
