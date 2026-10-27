import { describe, expect, it } from 'vitest';
import { BASE_BANK } from '../src/model';
// Independent JS algebra, not the Python Fraction/Decimal generator.
const evaluators: Record<string, {unit:string; precision:number; evaluate:(v:number[])=>number}> = {
 soluteMass:{unit:'g',precision:2,evaluate:v=>v[0]/100*v[1]},
 massPercent:{unit:'%',precision:2,evaluate:v=>100/(v[1]/v[0])},
 solventMass:{unit:'g',precision:2,evaluate:v=>v[0]*(1-v[1]/100)},
 dilutionStock:{unit:'mL',precision:2,evaluate:v=>v[2]/(v[0]/v[1])},
 dilutionWater:{unit:'mL',precision:2,evaluate:v=>v[1]*(v[0]/v[2]-1)},
 dilutionFinal:{unit:'mL',precision:2,evaluate:v=>v[1]/(v[2]/v[0])},
 mixturePercent:{unit:'%',precision:2,evaluate:v=>v[1]+(v[3]-v[1])*v[2]/(v[0]+v[2])},
 componentRatio:{unit:'g',precision:2,evaluate:v=>v[0]/(1+v[2]/v[1])},
 trayArea:{unit:'cm²',precision:0,evaluate:v=>v[2]*(v[0]*v[1])},
 containerVolume:{unit:'mL',precision:0,evaluate:v=>v[1]*v[0]},
 completeUses:{unit:'회',precision:0,evaluate:v=>Math.floor((v[0]-v[1])/v[2])},
 stageMinutes:{unit:'분',precision:0,evaluate:v=>v.reduce((sum,x)=>sum+x,0)},
 inventoryBalance:{unit:'개',precision:0,evaluate:v=>(v[0]-v[2])+(v[1]-v[3])},
 materialCost:{unit:'원',precision:0,evaluate:v=>v[0]*(v[2]/v[1])},
};
function halfUp(n:number,p:number) {
 const scale=10**p;
 return Math.round((n+Number.EPSILON*Math.max(1,n))*scale)/scale;
}
describe('700개 수치 조건 변형의 독립 검산',()=>{
 it('반올림 경계와 버림 조건을 구별한다',()=>{
  expect(halfUp(1.005,2)).toBe(1.01);
  expect(halfUp(14.325,2)).toBe(14.33);
  expect(halfUp(10.5,0)).toBe(11);
  expect(evaluators.completeUses.evaluate([30,4,3])).toBe(8);
 });
 it.each(BASE_BANK.filter(q=>q.calculation))('$id 공식·단위·조건·답안·동치 보기',q=>{
  const c=q.calculation!;
  const e=evaluators[c.kind]; expect(e).toBeDefined();
  expect(c.values.every(v=>Number.isFinite(v)&&v>0)).toBe(true);
  expect(c.unit).toBe(e.unit); expect(c.precision).toBe(e.precision);
  const expected=halfUp(e.evaluate(c.values),e.precision);
  expect(c.result).toBeCloseTo(expected,8);
  const options=q.choices.map(choice=>{
   const m=choice.match(/^([0-9]+(?:\.[0-9]+)?)\s+(.+)$/);
   expect(m).not.toBeNull(); expect(m![2]).toBe(e.unit);
   return Number(m![1]);
  });
  expect(options.every(x=>x>=0&&Number.isFinite(x))).toBe(true);
  expect(new Set(options).size).toBe(4);
  expect(options[q.answer-1]).toBeCloseTo(expected,8);
  expect(options.filter(x=>Math.abs(x-expected)<1e-8)).toHaveLength(1);
  expect(q.family).toBe(`NAIL-CALC-${c.kind}`);
  expect(q.question).toMatch(/가상|연습/);
  expect(q.explanation).toContain('기출 출제 사실을 뜻하지 않는다');
  expect(q.question).toContain(c.values[0].toString());
 });
});
