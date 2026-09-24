#!/usr/bin/env python3
import argparse, csv, json, sys
ALLOWED_LEVELS={'ĐỎ','CAM','VÀNG','XANH','XÁM'}
ALLOWED_RISK={'Rất nghiêm trọng','Nghiêm trọng','Trung bình','Nhẹ','Không ảnh hưởng'}
ALLOWED_P={'90','75','50','25','10'}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('csv'); ap.add_argument('--report',required=True); a=ap.parse_args()
    errors=[]; rows=0
    with open(a.csv,encoding='utf-8-sig',newline='') as f:
        for i,r in enumerate(csv.DictReader(f),2):
            rows+=1; k=r.get('Snapshot+ID','')
            if not k: errors.append({'row':i,'error':'missing Snapshot+ID'})
            if r.get('Mức độ tập trung') and r['Mức độ tập trung'] not in ALLOWED_LEVELS: errors.append({'row':i,'error':'invalid concentration level'})
            if r.get('Risk_Link_Status')=='MATCHED':
                if r.get('Mức hậu quả kinh tế') not in ALLOWED_RISK: errors.append({'row':i,'error':'invalid risk severity'})
                if r.get('Khả năng xảy ra (%)') not in ALLOWED_P: errors.append({'row':i,'error':'invalid probability'})
                if not r.get('Căn cứ xác suất','').strip(): errors.append({'row':i,'error':'missing probability evidence'})
            if r.get('Mức độ tập trung') in {'ĐỎ','XANH'} and r.get('Cần rà soát thủ công')!='Có': errors.append({'row':i,'error':'mandatory manual review missing'})
    report={'rows':rows,'errors':errors,'passed':not errors}
    with open(a.report,'w',encoding='utf-8') as f: json.dump(report,f,ensure_ascii=False,indent=2)
    print(json.dumps(report,ensure_ascii=False)); sys.exit(0 if not errors else 1)
if __name__=='__main__': main()
