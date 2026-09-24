#!/usr/bin/env python3
import argparse,csv,json,re,subprocess,sys,tempfile,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]; E=[]; W=[]
def ck(x,m):
    if not x:E.append(m)
def main():
    p=argparse.ArgumentParser(description='Run deterministic structural and integration QC for this skill package.')
    p.add_argument('--json-out'); a=p.parse_args()
    required=['SKILL.md','references/master-tracking-profile.md','references/results-rules.md','references/classification-rules.md','references/decision-record.md','scripts/profile_master_tracking.py','scripts/prepare_classification.py','scripts/validate_classification.py','evals/evals.json','evals/trigger-queries.json','evals/README.md','evals/grading-rubric.md','evals/benchmark-template.json','evals/files/master_tracking_fixture.xlsx']
    for f in required:ck((R/f).exists(),'missing '+f)
    ck(not any(R.rglob('__pycache__')),'package contains __pycache__')
    ck(not any(R.rglob('*.pyc')),'package contains .pyc')
    s=(R/'SKILL.md').read_text(encoding='utf-8');parts=s.split('---',2);ck(len(parts)==3,'invalid frontmatter delimiters')
    if len(parts)==3:
        name=re.search(r'^name: (.+)$',parts[1],re.M);desc=re.search(r'^description: (.+)$',parts[1],re.M)
        ck(bool(name),'missing name');ck(bool(desc),'missing description')
        if name:ck(name.group(1)==R.name,'name mismatch')
        if desc:ck(1<=len(desc.group(1))<=1024,'description length invalid')
    ck(len(s.splitlines())<500,'SKILL.md >=500 lines');ck(len(s.split())<5000,'SKILL.md >=5000 words')
    ev=json.loads((R/'evals/evals.json').read_text(encoding='utf-8'));ck(ev.get('skill_name')==R.name,'eval skill_name mismatch');ids=[]
    for x in ev.get('evals',[]):
        ids.append(x.get('id'));ck(bool(x.get('prompt')),'eval missing prompt');ck(bool(x.get('expected_output')),'eval missing expected_output');ck(isinstance(x.get('expectations'),list) and x['expectations'],'eval missing expectations')
        for f in x.get('files',[]):ck((R/f).exists(),f'eval input missing: {f}')
    ck(len(ids)==len(set(ids)),'duplicate eval ids')
    tr=json.loads((R/'evals/trigger-queries.json').read_text(encoding='utf-8'));pos=sum(x.get('should_trigger') is True for x in tr);neg=sum(x.get('should_trigger') is False for x in tr);ck(pos>=5 and neg>=5,'need >=5 positive and >=5 negative trigger cases')
    for sc in ['profile_master_tracking.py','prepare_classification.py','validate_classification.py']:
        q=subprocess.run([sys.executable,str(R/'scripts'/sc),'--help'],capture_output=True,text=True);ck(q.returncode==0 and 'usage:' in q.stdout.lower(),sc+' --help failed')
        q=subprocess.run([sys.executable,'-m','py_compile',str(R/'scripts'/sc)],capture_output=True,text=True);ck(q.returncode==0,sc+' compile failed')
    fixture=R/'evals/files/master_tracking_fixture.xlsx'
    with tempfile.TemporaryDirectory() as td:
        profile=Path(td)/'profile.json';plan=Path(td)/'plan.json'
        q=subprocess.run([sys.executable,str(R/'scripts/profile_master_tracking.py'),str(fixture),'--output',str(profile)],capture_output=True,text=True);ck(q.returncode==0,'profile fixture failed')
        q=subprocess.run([sys.executable,str(R/'scripts/prepare_classification.py'),str(fixture),'--output',str(plan)],capture_output=True,text=True);ck(q.returncode==0,'prepare fixture failed')
        if profile.exists() and plan.exists():
            pr=json.loads(profile.read_text(encoding='utf-8'));pl=json.loads(plan.read_text(encoding='utf-8'));items=pl.get('items',[])
            ck(pr.get('header_row')==3,'header row must be 3');ck(pr.get('data_start_row')==4,'data start row must be 4')
            ck(pr.get('row_count')==445,'fixture row count drift');ck(pr.get('stable_id_count')==241,'fixture stable ID count drift');ck(len(items)==241,'plan must contain 241 IDs')
            ck(len({x.get('id') for x in items})==len(items),'plan has duplicate IDs')
            ck(all(isinstance(x.get('source_rows'),list) and x['source_rows'] and all(r.get('sheet') and isinstance(r.get('row'),int) and isinstance(r.get('master_row'),int) for r in x['source_rows']) for x in items),'source trace incomplete')
            ck(all(x.get('latest_snapshot') for x in items),'latest snapshot missing')
            ck(all(x.get('rule_based_candidate') in {'ĐỎ','CAM','VÀNG','XANH','XÁM','REVIEW_FOR_XANH_OR_VÀNG','REVIEW_FOR_RED_OR_ORANGE'} for x in items),'unexpected candidate')
        good=Path(td)/'good.csv';bad=Path(td)/'bad.csv'
        fields=['ID','Mức độ tập trung','Căn cứ phân loại','Cách xử lý','Cần rà soát thủ công']
        with good.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerow({'ID':'A','Mức độ tập trung':'CAM','Căn cứ phân loại':'Quá hạn, đầu ra chưa hoàn tất.','Cách xử lý':'Theo dõi hằng tuần và yêu cầu ngày hoàn thành mới.','Cần rà soát thủ công':'Không'})
        with bad.open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerow({'ID':'B','Mức độ tập trung':'ĐỎ','Căn cứ phân loại':'Quá hạn.','Cách xử lý':'Theo dõi.','Cần rà soát thủ công':'Không'})
        q=subprocess.run([sys.executable,str(R/'scripts/validate_classification.py'),str(good)],capture_output=True,text=True);ck(q.returncode==0,'validator rejected valid fixture')
        q=subprocess.run([sys.executable,str(R/'scripts/validate_classification.py'),str(bad)],capture_output=True,text=True);ck(q.returncode==2,'validator failed to reject invalid red fixture')
    W.append('External isolated with-skill versus baseline runs are still pending; no benchmark pass rate is claimed.')
    out={'status':'pass' if not E else 'fail','error_count':len(E),'errors':E,'warnings':W,'eval_count':len(ids),'positive_trigger_count':pos,'negative_trigger_count':neg}
    text=json.dumps(out,ensure_ascii=False,indent=2);print(text)
    if a.json_out:Path(a.json_out).write_text(text+'\n',encoding='utf-8')
    return 0 if not E else 2
if __name__=='__main__':raise SystemExit(main())
