#!/usr/bin/env python3
import argparse, csv, json, re

RISK_COL = 'Mức độ nghiêm trọng của hậu quả (tiền, thời gian, con người) và khả năng sinh ra rủi ro'
KEY = 'Snapshot+ID'
LEVELS = 'Rất nghiêm trọng|Nghiêm trọng|Trung bình|Nhẹ|Không ảnh hưởng'
PAT = re.compile(r'Hậu quả\s*[–-]\s*(' + LEVELS + r')\s*:\s*(.*?)\s*(?:<br>|\n)\s*Khả năng xảy ra\s*[–-]\s*(90|75|50|25|10)%\s*:\s*(.*)', re.I | re.S)
AMOUNT = re.compile(r'((?:từ\s+|dưới\s+)?\d+(?:[.,]\d+)?(?:\s*[–-]\s*\d+(?:[.,]\d+)?)?\s*(?:triệu|tỷ)\s*đồng)', re.I)

def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('classification_csv')
    ap.add_argument('risk_csv')
    ap.add_argument('--output', required=True)
    ap.add_argument('--report', required=True)
    a = ap.parse_args()
    base, risk = read_csv(a.classification_csv), read_csv(a.risk_csv)
    index, dup = {}, set()
    for r in risk:
        k = (r.get(KEY) or '').strip()
        if not k: continue
        if k in index: dup.add(k)
        else: index[k] = r
    out, stats = [], {'matched':0,'missing':0,'duplicate':0,'invalid_format':0}
    for row in base:
        k = (row.get(KEY) or '').strip()
        nr = dict(row)
        text = ''
        if k in dup:
            status='DUPLICATE'; stats['duplicate']+=1
        elif k not in index:
            status='MISSING'; stats['missing']+=1
        else:
            text=(index[k].get(RISK_COL) or '').strip()
            m=PAT.search(text)
            if not m:
                status='INVALID_FORMAT'; stats['invalid_format']+=1
            else:
                status='MATCHED'; stats['matched']+=1
                level, consequence, probability, evidence = m.groups()
                amount = AMOUNT.search(consequence)
                nr['Mức hậu quả kinh tế']=level
                nr['Giá trị kinh tế phơi nhiễm']=amount.group(1) if amount else ''
                nr['Khả năng xảy ra (%)']=probability
                nr['Căn cứ xác suất']=evidence.strip()
                nr['Risk_Estimate_Type']='SCREENING' if 'ước tính' in consequence.lower() else 'DIRECT_OR_CALCULATED'
        nr['Risk_Link_Status']=status
        nr['Risk_Source_Text']=text
        if status != 'MATCHED': nr['Cần rà soát thủ công']='Có'
        out.append(nr)
    fields=[]
    for r in out:
        for k in r:
            if k not in fields: fields.append(k)
    with open(a.output,'w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(out)
    with open(a.report,'w',encoding='utf-8') as f: json.dump(stats,f,ensure_ascii=False,indent=2)
    print(json.dumps(stats,ensure_ascii=False))
if __name__=='__main__': main()
