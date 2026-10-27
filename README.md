# Craftsman-Nail-Technician-CBT

미용사(네일) 필기 CBT 비공식 학습 앱. React·TypeScript·Vite 정적 사이트이며 로그인·서버·유료 API가 없다.

전기기능사 CBT의 고정 앱 커밋을 실제 재사용했고, 최신 main의 cbt-site-standard v1.4.0을 적용했다.
학습 기준 선택 메뉴는 없으며 실전·랜덤 모두 응답 후 Space로 다음 문제를 이동한다.
마지막 시험 문제에서 Space는 제출하지 않는다. 답안 선택·이동 후 본문으로 포커스를 옮기고
입력 컨트롤·메뉴·대화상자·반복 키 입력을 보호한다.

실전 시험(절대 종료시각, 새로고침 복구, 만료 자동 제출, 제출 확인, 결과와 해설),
랜덤 즉시 채점·연속 정답·오답 복습, 북마크·통계·학습 이어하기,
JSON/CSV 등록·중복 제거·검증 대기·근거 입력 후 로컬 승인·내보내기를 제공한다.
모바일 메뉴는 작은 높이·가로 화면에서 내부 스크롤하며 하단 백업/초기화와 상단 메뉴에 접근할 수 있다.

공식 규칙 확인과 문제은행 수량은 미완료다. [출처·검수 기록](docs/sources.md)을 먼저 확인한다.
현재 학습용 설정은 60문항·60분·4지선다·60점 이상 합격·과락 없음·미응답 오답이다.
Q-Net 접근이 프록시 403으로 차단되어 공식 시험 규칙으로 확인하지 못했다.
공식 과목 배분을 주장하지 않고 `네일미용 통합`에서 무작위 추출한다.

문제은행은 **자체 제작·내부 검토 60문항**(다섯 학습 영역 각 12), 기출 0, 복원 0,
숫자 변형 0, 검증 대기 0. 목표 1,000에 **940 부족**하며 표준 수량 미충족이다.
외부 전문가 검수·공식 기준 대조는 미완료이며 전문가 검수 완료 수는 0이다.
연도·회차는 창작하지 않았고 모든 문항이 null이다. MIT 앱 코드와 CC BY 4.0 자체 문항의
이용 조건은 [LICENSE](LICENSE)에 있다.

## 로컬 개발

Node.js 24.19.0 (`.node-version`), npm lockfile 사용.

```sh
cd /workspace/Craftsman-Nail-Technician-CBT
npm ci
npm run dev -- --port 5173 --strictPort
```

```sh
npm test
npm run build
npx playwright install chromium
npm run test:e2e
```

시스템 Chromium 사용 시 `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium npm run test:e2e`.
`python3 scripts/author-bank.py`는 동일한 기본 JSON을 재생성한다.
새 Git worktree는 만들 필요 없이 현재 격리된 체크아웃을 사용한다.

검증 범위와 실제 배포 상태: [검증 기록](docs/validation.md), [배포 기록](docs/deployment.md).

## 저장·개인정보

localStorage namespace는 `Craftsman-Nail-Technician-CBT:v1`이며 전기기능사와 분리한다.
최근 응답 5,000개, 시험 결과 30회와 진행 중 시험·랜덤 세션·북마크·오답·로컬 문항을 저장한다.
통계는 이 보관 범위와 현재 브라우저 기준이다. 초기화는 확인 후 로컬 자료를 지우며 기본 은행은 유지한다.
JSON 기록 백업은 제공하지만 백업 복원 UI는 제공하지 않는다.
손상 원본 자동 덮어쓰기를 막고 저장 실패를 알린다. 저장 제한/시크릿 모드/iframe에서는
저장이 제한될 수 있고 origin이 달라지면 기록이 분리된다.

## 자동 배포 준비

main push → 단위 검사·빌드·PC/모바일 브라우저 검증 성공 → Pages 자동 배포.
PR은 검증만 수행한다. 최초 Pages Source 설정과 권한 확인이 필요하다.
사용자의 요청에 따라 첫 배포 사전 확인 거부 또는 첫 파이프라인 실패 후에는
재실행·대체 경로·배포를 유발하는 추가 push를 하지 않는다.

예상 기본 주소: https://YunSangYeong.github.io/Craftsman-Nail-Technician-CBT/
이 주소 표시는 배포 성공이나 공개 화면 확인의 증거가 아니다.
