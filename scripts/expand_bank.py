"""Fixed authored manuscripts + explicit numeric condition variants.
No external source, year or session is invented. Numerical data are exercises,
not actual product dilution instructions or legal specifications.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPTS = [
    ('overview.txt', '네일 개론'), ('anatomy.txt', '피부·손발톱'),
    ('hygiene.txt', '위생·안전'), ('materials.txt', '화장품·재료'),
    ('technique.txt', '네일 기술'),
]

def fmt(value):
    d = Decimal(value.numerator) / Decimal(value.denominator) if isinstance(value, Fraction) else Decimal(str(value))
    return format(d.normalize(), 'f')

def rounded(value, precision):
    d = Decimal(value.numerator) / Decimal(value.denominator) if isinstance(value, Fraction) else Decimal(str(value))
    return d.quantize(Decimal(1).scaleb(-precision), rounding=ROUND_HALF_UP)

def question(id, topic, stem, correct, distractors, explanation, index, **extra):
    choices = [correct, *distractors]
    assert len(set(choices)) == 4, id
    offset = index % 4
    choices = choices[offset:] + choices[:offset]
    return dict(id=id, subject='네일미용 통합', topic=topic, question=stem,
        choices=choices, answer=choices.index(correct)+1, explanation=explanation,
        difficulty='중', year=None, session=None, type='original',
        sourceUrl='https://github.com/YunSangYeong/Craftsman-Nail-Technician-CBT/blob/main/docs/sources.md',
        verificationStatus='reviewed',
        reviewNote='AI 일반 지식 기반 자체 제작. 문장·보기·정답 논리 내부검토; 외부 전문가 검수·공식 출제기준 대조 미완료. 저장소는 작성 위치이며 외부 정답 증빙이 아님.' + (' 계산은 독립 테스트로 재검산. 숫자 조건 변형이며 기출·독립 개념 수가 아님.' if extra.get('family') else ''),
        version='nail-main', rights='자체 제작 학습 문항 · CC BY 4.0 · Craftsman-Nail-Technician-CBT contributors', **extra)

def concepts():
    result=[]
    for file,topic in MANUSCRIPTS:
        lines=(ROOT/'scripts/manuscripts'/file).read_text().splitlines()
        assert len(lines)==48, (file,len(lines))
        for line in lines:
            stem,correct,d1,d2,d3,explanation=line.split('|')
            i=len(result)+1
            result.append(question(f'NAIL-CON-{i:03}',topic,stem,correct,[d1,d2,d3],explanation,i-1))
    return result


def numeric_case(kind, n):
    """Return topic, stem, exact rational answer, unit, inputs, derivation, precision."""
    if kind=='soluteMass':
        total,percent=100+20*n,2+n%8
        exact=Fraction(total*percent,100)
        return '화장품·재료',f'질량 백분율 {percent}%의 가상 화장품 혼합물 {total} g에 들어 있는 성분 A의 질량은?',exact,'g',[total,percent],f'성분 질량=총질량×질량분율={total}×{percent}/100',2
    if kind=='massPercent':
        total=100+10*n; solute=Fraction(total*(2+n%12),100)
        exact=solute/total*100
        return '화장품·재료',f'가상 혼합물의 총질량이 {total} g이고 성분 A가 {fmt(solute)} g일 때 A의 질량 백분율은?',exact,'%', [float(solute),total],f'질량 백분율=성분 질량/총질량×100={fmt(solute)}/{total}×100',2
    if kind=='solventMass':
        total,percent=150+10*n,5+n%12; exact=Fraction(total*(100-percent),100)
        return '화장품·재료',f'A와 용매만으로 된 가상 혼합물 {total} g에서 A의 질량 백분율이 {percent}%일 때 용매 질량은?',exact,'g',[total,percent],f'용매 질량=총질량−A 질량={total}−{total}×{percent}/100',2
    if kind=='dilutionStock':
        stock,target,final=20+10*(n%5),1+n%8,100+20*n
        exact=Fraction(target*final,stock)
        return '화장품·재료',f'가상 부피 농도 계산에서 {stock}% 원액으로 {target}% 혼합물 {final} mL를 만든다. 필요한 원액 부피는? 최종 부피 기준이며 실제 제품 처방이 아니다.',exact,'mL',[stock,target,final],f'원액 농도×원액 부피=최종 농도×최종 부피. 원액 부피={target}×{final}/{stock}',2
    if kind=='dilutionWater':
        stock,target,v=50,5+5*(n%3),10+2*n; exact=Fraction(stock*v,target)-v
        return '화장품·재료',f'부피가 단순 합산된다고 가정한 연습이다. 가상 {stock}% 액체 {v} mL를 물로 {target}%로 낮출 때 추가 물의 부피는? 실제 제품 사용 지침이 아니다.',exact,'mL',[stock,v,target],f'최종 부피={stock}×{v}/{target}. 추가 물=최종 부피−원액 부피={stock}×{v}/{target}−{v}',2
    if kind=='dilutionFinal':
        stock,target,v=20+20*(n%3),4+n%7,12+2*n; exact=Fraction(stock*v,target)
        return '화장품·재료',f'가상 부피 농도 계산에서 {stock}% 액체 {v} mL에 물을 더해 {target}%로 맞춘다. 필요한 최종 혼합물 부피는? 원액 성분 손실은 없고 실제 조제 지침이 아니다.',exact,'mL',[stock,v,target],f'성분량 보존으로 최종 부피=원액 농도×원액 부피/최종 농도={stock}×{v}/{target}',2
    if kind=='mixturePercent':
        v1,c1,v2,c2=40+2*n,10+2*(n%5),60+3*n,2+n%3
        exact=Fraction(v1*c1+v2*c2,v1+v2)
        return '화장품·재료',f'같은 성분 A의 가상 용액을 혼합한다. {c1}% 용액 {v1} mL와 {c2}% 용액 {v2} mL를 섞으면 부피 백분율은? 부피 단순 합산·반응 없음 가정이다.',exact,'%', [v1,c1,v2,c2],f'전체 A 부피/전체 혼합물 부피×100=({v1}×{c1}+{v2}×{c2})/({v1}+{v2})',2
    if kind=='componentRatio':
        total,a,b=30+3*n,1+n%4,2+n%5; exact=Fraction(total*a,a+b)
        return '화장품·재료',f'가상 실습 재료 A:B의 질량비가 {a}:{b}이다. 합계 {total} g을 만들 때 A의 질량은? 실제 아크릴 제품 배합비를 뜻하지 않는다.',exact,'g',[total,a,b],f'전체 비율 단위={a}+{b}. A 질량=총질량×A 비율/비율 합={total}×{a}/({a}+{b})',2
    if kind=='trayArea':
        w,h,count=20+n,30+2*n,2+n%3; exact=Fraction(w*h*count)
        return '위생·안전',f'청소 면적 산출 연습이다. 가로 {w} cm, 세로 {h} cm인 직사각형 작업 트레이 {count}개의 윗면 총면적은? 측면은 제외한다.',exact,'cm²',[w,h,count],f'한 윗면 면적=가로×세로. 총면적={w}×{h}×{count}',0
    if kind=='containerVolume':
        count,each=2+n%8,100+10*n; exact=Fraction(count*each)
        return '위생·안전',f'가상 작업 계획에서 별도 용기 {count}개에 준비된 작업액을 각각 {each} mL씩 배분한다. 손실 없이 필요한 작업액 총부피는? 제품 농도·접촉 시간을 지정하는 문제가 아니다.',exact,'mL',[count,each],f'필요 총부피=용기 수×용기당 부피={count}×{each}',0
    if kind=='completeUses':
        total,reserve,each=30+5*n,3+n%4,2+n%5; exact=Fraction((total-reserve)//each)
        return '네일 기술',f'사용량 계산 연습이다. 가상 제품 {total} g 중 {reserve} g을 사용하지 않고 남긴다. 1회당 정확히 {each} g을 쓰고 손실이 없으면 완전히 제공 가능한 횟수는?',exact,'회',[total,reserve,each],f'사용 가능량={total}−{reserve}={total-reserve} g. 완전한 횟수=⌊{total-reserve}/{each}⌋',0
    if kind=='stageMinutes':
        a,b,c,d=5+n%6,10+n%8,8+n%10,3+n%5; exact=Fraction(a+b+c+d)
        return '네일 기술',f'가상 예약 계획에서 상담 {a}분, 준비 {b}분, 디자인 {c}분, 마무리 {d}분을 겹침 없이 차례로 한다. 합계 작업 시간은? 젤 경화 시간 지침이 아니다.',exact,'분',[a,b,c,d],f'순차 작업 총시간=각 단계 시간의 합={a}+{b}+{c}+{d}',0
    if kind=='inventoryBalance':
        start,incoming,used,damaged=20+2*n,5+n%7,3+n%9,1+n%3; exact=Fraction(start+incoming-used-damaged)
        return '네일 개론',f'가상 재고 계산 연습이다. 일회용 버퍼 재고가 {start}개였다. {incoming}개 입고, {used}개 사용, 미사용 불량품 {damaged}개 폐기 후 사용 가능한 재고는? 각 수량은 서로 중복되지 않는다.',exact,'개',[start,incoming,used,damaged],f'가용 재고=기초+입고−사용−불량 폐기={start}+{incoming}−{used}−{damaged}',0
    if kind=='materialCost':
        price,total,used=9000+330*n,50+2*n,2+n%5; exact=Fraction(price*used,total)
        return '네일 개론',f'재료비 산출 연습이다. 가상 제품 {total} mL의 가격이 {price}원이고 1회에 {used} mL를 사용한다. 손실·세금·기타 비용을 제외한 1회 제품 재료비는?',exact,'원',[price,total,used],f'mL당 가격=전체 가격/전체 부피. 1회 재료비={price}/{total}×{used}',0
    raise ValueError(kind)

KINDS=['soluteMass','massPercent','solventMass','dilutionStock','dilutionWater','dilutionFinal','mixturePercent','componentRatio','trayArea','containerVolume','completeUses','stageMinutes','inventoryBalance','materialCost']

def calculations():
    result=[]
    for family_index, kind in enumerate(KINDS,1):
        for n in range(1,51):
            topic,stem,exact,unit,values,derivation,precision=numeric_case(kind,n)
            value=rounded(exact,precision)
            step=Decimal(1) if precision==0 else max(Decimal('0.1'),rounded(value/10,2))
            candidates=[value-step, value+step, value+2*step, value+3*step]
            wrong=[]
            for x in candidates:
                x=rounded(x,precision)
                if x>=0 and x!=value and x not in wrong: wrong.append(x)
                if len(wrong)==3: break
            assert len(wrong)==3
            round_note='원 미만은 일반 반올림한다.' if unit=='원' else ('소수 셋째 자리에서 일반 반올림하여 소수 둘째 자리까지 답한다.' if precision==2 else '정수로 답한다.')
            stem+=' '+round_note
            explanation=f'{derivation}={fmt(value)} {unit}. '+('나머지는 1회 사용량을 채우지 못하므로 버림한다. ' if kind=='completeUses' else '')+round_note+' 주어진 가정에서의 실습 계산이며 실제 제품 처방·법정 기준이나 기출 출제 사실을 뜻하지 않는다.'
            result.append(question(f'NAIL-CALC-{family_index:02}-{n:03}',topic,stem,f'{fmt(value)} {unit}',[f'{fmt(x)} {unit}' for x in wrong],explanation,n+family_index-2,
                family=f'NAIL-CALC-{kind}',calculation=dict(kind=kind,values=values,result=float(value),unit=unit,precision=precision)))
    return result


def create_additions():
    return concepts()+calculations()
