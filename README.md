# phan-loai-muc-do-tap-trung-giam-sat-linked

Bản điều chỉnh để liên kết kết quả của skill `danh-gia-rui-ro` vào quy trình phân loại `Mức độ tập trung`.

## Điểm thay đổi chính

- Dùng `Snapshot+ID` làm khóa nối duy nhất.
- Tách hậu quả kinh tế, giá trị phơi nhiễm, xác suất và căn cứ xác suất thành các trường riêng.
- Không ánh xạ cơ học `Rất nghiêm trọng = ĐỎ`.
- ĐỎ cần thêm tính tức thời và nhu cầu can thiệp cấp thẩm quyền.
- XANH cần bằng chứng phơi nhiễm kinh tế đã được loại bỏ hoặc chấp nhận.
- Thêm cổng rà soát thủ công cho ĐỎ, XANH, hậu quả Rất nghiêm trọng và lỗi liên kết.

## Tích hợp vào repository hiện hữu

Sao chép đè `SKILL.md`, rồi thêm:

- `references/risk-integration-contract.md`
- `scripts/link_risk_results.py`
- `scripts/validate_risk_linkage.py`
- các eval tích hợp vào bộ eval hiện hữu.

Repository nguồn: https://github.com/ducle2502/phan-loai-muc-do-tap-trung-giam-sat
