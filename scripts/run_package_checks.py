#!/usr/bin/env python3
import json,re,subprocess,sys,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];E=[]
def ck(x,m):
 if not x:E.append(m)
for f in ['SKILL.md','references/classification-rules.md','references/decision-record.md','scripts/prepare_classification.py','scripts/validate_classification.py','evals/evals.json','evals/trigger-queries.json','evals/history.json','evals/files/cases.csv']:ck((R/f).exists(),'missing '+f)
s=(R/'SKILL.md').read_text(encoding='utf-8');parts=s.split('---',2);ck(len(parts)==3,'frontmatter')
if len(parts)==3:
 name=re.search(r'^name: (.+)$',parts[1],re.M);desc=re.search(r'^description: (.+)$',parts[1],re.M);ck(bool(name),'name');ck(bool(desc),'description')
 if name:ck(name.group(1)==R.name,'name mismatch')
 if desc:ck(len(desc.group(1))<=1024,'description too long')
ck(len(s.splitlines())<500,'too many lines');ck(len(s.split())<5000,'too many words')
ev=json.loads((R/'evals/evals.json').read_text(encoding='utf-8'));ids=[]
for x in ev['evals']:ids.append(x['id']);ck(bool(x.get('expectations')),'missing expectations')
ck(len(ids)==len(set(ids)),'duplicate ids')
tr=json.loads((R/'evals/trigger-queries.json').read_text(encoding='utf-8'));pos=sum(x['should_trigger'] is True for x in tr);neg=sum(x['should_trigger'] is False for x in tr);ck(pos>=5 and neg>=5,'trigger coverage')
for sc in ['prepare_classification.py','validate_classification.py']:
 q=subprocess.run([sys.executable,str(R/'scripts'/sc),'--help'],capture_output=True,text=True);ck(q.returncode==0 and 'usage:' in q.stdout.lower(),sc+' help')
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'p.json';q=subprocess.run([sys.executable,str(R/'scripts/prepare_classification.py'),str(R/'evals/files/cases.csv'),'--output',str(p)],capture_output=True,text=True);ck(q.returncode==0,'fixture')
 if p.exists():
  c={x['id']:x['rule_based_candidate'] for x in json.loads(p.read_text(encoding='utf-8'))['items']};ck(c.get('ORANGE')=='CAM','orange');ck(c.get('GRAY')=='XÁM','gray');ck(c.get('YELLOW')=='VÀNG','yellow')
out={'status':'pass' if not E else 'fail','error_count':len(E),'errors':E,'eval_count':len(ids),'positive_trigger_count':pos,'negative_trigger_count':neg};print(json.dumps(out,ensure_ascii=False,indent=2));raise SystemExit(0 if not E else 2)
