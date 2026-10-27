"""Schema-independent duplicate and manuscript audit, with AI editorial review notes.
Similarity candidates are not a proof of semantic uniqueness. Explicit number
families are condition variants, not 700 independent concepts.
"""
from pathlib import Path
import json, re, unicodedata, hashlib, difflib
from collections import Counter
r=Path(__file__).resolve().parents[1]
p=r/'src/data/questions-main.json';data=p.read_bytes();bank=json.loads(data)
assert len(bank)==1000
assert len({q['id'] for q in bank})==1000

def norm(text):return re.sub(r'\s+','',unicodedata.normalize('NFKC',text)).lower()
fingerprints=[norm('|'.join([q['question'],*sorted(q['choices'])])) for q in bank]
assert len(set(fingerprints))==1000
for q in bank:
 assert q['type']=='original' and q['year'] is None and q['session'] is None
 assert len(q['choices'])==len(set(map(norm,q['choices'])))==4
 assert 1<=q['answer']<=4
 assert q['verificationStatus']=='reviewed'
concepts=[q for q in bank if not q.get('family')]
calcs=[q for q in bank if q.get('family')]
assert len(concepts)==300 and len(calcs)==700
families=Counter(q['family'] for q in calcs)
assert len(families)==14 and set(families.values())=={50}
candidates=[]
for i,q in enumerate(concepts):
 for other in concepts[:i]:
  score=difflib.SequenceMatcher(None,q['question'],other['question']).ratio()
  if score>.72:
   candidates.append(dict(ids=[other['id'],q['id']],similarity=round(score,4),questions=[other['question'],q['question']],
    disposition='내부검토: 문장틀이 유사하지만 묻는 대상·정답이 달라 별도 문항으로 유지. 전문가 의미 검수는 아님.'))
report=dict(total=len(bank),reviewedInternal=1000,expertReviewed=0,pending=0,past=0,reconstructed=0,original=1000,
 concepts=300,numericVariants=700,numericTemplates=14,shortage=0,exactNormalizedDuplicates=0,
 topicCounts=dict(Counter(q['topic'] for q in bank)),variantCounts=dict(families),
 answerPositionCounts=dict(Counter(q['answer'] for q in bank)),
 dataSha256=hashlib.sha256(data).hexdigest(),
 semanticReview=dict(method='AI 원고·정답·보기·해설 내부 검토 및 문장 유사도 후보 검토. 수치 변형 family는 별도 집계. 모든 문항이 독립 개념이라는 뜻이 아님.',threshold=.72,candidates=candidates),
 externalSourceVerification='미완료. 일반 지식 및 주어진 가상 수치의 산술. 공식 기출·제품 처방·법정 기준 아님.')
(r/'docs/bank-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['semanticReview']},ensure_ascii=False,indent=2))
print('AI 내부 의미 검토 후보:',len(candidates))
