#!/usr/bin/env python3
import argparse,csv,json,re,sys
from pathlib import Path
A={'ĐỎ','CAM','VÀNG','XANH','XÁM'};T={'có','co','yes','true','1'};R=('Mức độ tập trung','Căn cứ phân loại','Cách xử lý')
def main():
 p=argparse.ArgumentParser(description='Validate supervisory classifications.');p.add_argument('input');p.add_argument('--report');a=p.parse_args();path=Path(a.input)
 if not path.exists():return 3
 with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 if not rows:return 4
 miss=[x for x in R if x not in rows[0]]
 if miss:return 5
 issues=[]
 for i,r in enumerate(rows,2):
  key=(r.get('ID') or f'row-{i}').strip();level=(r.get(R[0]) or '').strip().upper();basis=(r.get(R[1]) or '').strip();action=(r.get(R[2]) or '').strip();review=(r.get('Cần rà soát thủ công') or '').strip().lower()
  def add(c,m):issues.append({'row':i,'id':key,'code':c,'message':m})
  if level not in A:add('invalid_level','invalid level')
  if not basis:add('missing_basis','blank basis')
  if not action:add('missing_action','blank action')
  if level=='ĐỎ' and review not in T:add('red_requires_review','ĐỎ requires review')
  if level=='XANH' and re.search(r'\b(đóng|xóa|xoá|kết thúc)\b',action,re.I) and review not in T:add('green_closure_requires_review','closure requires review')
  if level=='XÁM' and re.search(r'\b(ít rủi ro|an toàn|đã kiểm soát|hoàn thành)\b',basis,re.I):add('gray_misinterpreted','XÁM is not low risk')
  if level=='XANH' and re.search(r'\b(chưa có bằng chứng|đang chờ|chưa rõ|không có cập nhật)\b',basis,re.I):add('green_without_evidence','XANH needs positive evidence')
 result={'status':'pass' if not issues else 'fail','rows_checked':len(rows),'error_count':len(issues),'issues':issues};text=json.dumps(result,ensure_ascii=False,indent=2);print(text)
 if a.report:Path(a.report).write_text(text+'\n',encoding='utf-8')
 return 0 if not issues else 2
if __name__=='__main__':raise SystemExit(main())
