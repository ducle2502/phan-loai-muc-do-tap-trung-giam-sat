#!/usr/bin/env python3
import argparse,csv,json,re,sys
from datetime import datetime
from pathlib import Path
F=("%d/%m/%Y","%m/%d/%Y","%Y-%m-%d"); T={"x","✓","1","true","yes","có","co"}
def n(v):return re.sub(r"\s+"," ",(v or "").strip()).casefold()
def b(v):return n(v) in T
def d(v):
 for f in F:
  try:return datetime.strptime((v or '').strip(),f).date()
  except ValueError:pass
 return None
def main():
 p=argparse.ArgumentParser(description='Create per-ID supervisory classification plan; candidates are not final.');p.add_argument('input');p.add_argument('--output','-o');a=p.parse_args();path=Path(a.input)
 if not path.exists():print('ERROR input_not_found',file=sys.stderr);return 3
 with path.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 if not rows:return 4
 req={'Snapshot','ID','Tóm tắt nội dung chỉ đạo','Kết quả/tiến độ đến thời điểm báo cáo'};miss=sorted(req-set(rows[0]))
 if miss:print('ERROR missing_columns: '+', '.join(miss),file=sys.stderr);return 5
 g={}
 for i,r in enumerate(rows,2):
  dt=d(r.get('Snapshot'));key=(r.get('ID') or '').strip()
  if not dt or not key:return 6
  r['_row']=i;r['_date']=dt.isoformat();g.setdefault(key,[]).append(r)
 items=[]
 for key,h in sorted(g.items()):
  h.sort(key=lambda x:x['_date']);r=h[-1];prog=n(r.get('Kết quả/tiến độ đến thời điểm báo cáo'));pic=n(r.get('Chịu trách nhiệm (PIC)') or r.get('Chịu trách nhiệm'));days=n(r.get('Số ngày còn lại'));deadline=n(r.get('Thời hạn mới nhất (Date)') or r.get('Thời hạn (RAW)'));forecast=n(r.get('Dự kiến mới nhất (Date)') or r.get('Dự kiến thời gian hoàn thành (RAW)'));sig=[]
  if 'trễ hạn' in days or re.fullmatch(r'-\d+(?:\.0+)?',days):sig+=['overdue']
  if not deadline or 'không giao thời hạn' in days:sig+=['deadline_missing']
  if not forecast or 'chưa có dự kiến' in forecast:sig+=['forecast_missing']
  if not pic or pic in {'các đơn vị liên quan','đơn vị liên quan'}:sig+=['pic_unclear']
  if not prog or prog in {'đã nhận chỉ đạo','thực hiện theo chỉ đạo'}:sig+=['progress_uninformative']
  if re.search(r'\b(đang|chờ|dự kiến|phối hợp)\b',prog):sig+=['activity_not_output']
  if b(r.get('Hoàn Thành')) and re.search(r'\b(đang|chờ|đã chuyển|phối hợp|đề xuất ngừng)\b',prog):sig+=['completion_conflict']
  if len(h)>1 and prog==n(h[-2].get('Kết quả/tiến độ đến thời điểm báo cáo')):sig+=['no_substantive_progress']
  try:
   if float((r.get('Chênh lệch dự kiến so với thời hạn (Ngày)') or '').strip())>0:sig+=['forecast_after_deadline']
  except ValueError:pass
  facts={'output_identifiable':bool(n(r.get('Tóm tắt nội dung chỉ đạo'))),'timing_identifiable':bool(deadline),'progress_informative':bool(prog and 'progress_uninformative' not in sig),'pic_identifiable':bool(pic and 'pic_unclear' not in sig)}
  if not facts['output_identifiable'] or (not facts['timing_identifiable'] and not facts['progress_informative'] and not facts['pic_identifiable']):cand='XÁM'
  elif set(sig)&{'overdue','forecast_after_deadline','completion_conflict'}:cand='CAM'
  elif set(sig)&{'activity_not_output','forecast_missing','pic_unclear','deadline_missing'}:cand='VÀNG'
  else:cand='REVIEW_FOR_XANH_OR_VÀNG'
  items.append({'id':key,'latest_snapshot':r['_date'],'snapshot_count':len(h),'source_rows':[x['_row'] for x in h],'minimum_facts':facts,'observed_signals':sorted(set(sig)),'rule_based_candidate':cand,'red_assessment_required':True,'current':{k:v for k,v in r.items() if not k.startswith('_')}})
 out={'schema_version':'1.0','warning':'Candidates are not final. ĐỎ needs severity plus authority assessment; XANH needs positive evidence.','items':items};text=json.dumps(out,ensure_ascii=False,indent=2)
 if a.output:Path(a.output).write_text(text+'\n',encoding='utf-8');print(json.dumps({'status':'ok','items':len(items)},ensure_ascii=False))
 else:print(text)
 return 0
if __name__=='__main__':raise SystemExit(main())
