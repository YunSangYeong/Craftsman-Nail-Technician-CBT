# GitHub 반영·배포 상태

2026-10-27. 사용자 배포 요청과 v1.4.0의 첫 차단 시 중단 정책을 적용했다.

## 최초 사전 확인: 차단

- Git 원격 `main` 읽기: 성공, `b5477488c676e741ff73f8357b0b5963a56e982f`.
- 기존 체크아웃에는 앱·workflow·Pages 배포 설정 파일이 없었다.
- `GH_TOKEN` 변수와 GitHub CLI의 존재는 확인했으나 값은 읽거나 출력하지 않았다.
- Pages Source/권한 확인 대상: `https://api.github.com/repos/YunSangYeong/Craftsman-Nail-Technician-CBT/pages`.
- 실제 첫 요청: `curl: (56) CONNECT tunnel failed, response 403`, curl 종료 코드 56, HTTP 코드 000.
- API 서버 응답 이전의 프록시 차단이다. GitHub가 권한을 거절했다거나 Pages가 비활성이라고
  단정하지 않는다. Git 읽기 성공은 Pages API/Actions/푸시 권한의 증거가 아니다.

첫 차단 후 API 재조회, 다른 인증/도구 경로, main push, workflow 수동 실행·재실행,
대체 배포를 하지 않았다. 최초 CI 파이프라인도 시작하지 않았다.
기존 게시 상태는 미확인이고 이번 작업으로 배포한 것은 없다. 공개 화면도 확인하지 않았다.

코드는 자동 배포를 유발하지 않는 `feat/nail-cbt-standard` 브랜치로 보존한다.
준비한 workflow는 main push에서 validate 성공 후 deploy, PR에서는 validate만 수행한다.
이번 브랜치 push는 main 트리거에 해당하지 않으며 PR도 생성하지 않는다.
workflow 자체를 원격 실행해 검증한 것은 아니다.

사용자가 지금 할 최소 동작: **클라우드 환경 설정의 네트워크 허용 도메인에
`api.github.com`을 추가**한다. 이 동작은 첫 차단의 네트워크 선행조건을 다루는 것이며,
GitHub API 권한이나 Pages Source 설정까지 보장하지 않는다. 이후 배포 마무리는 사용자가 맡는다.
에이전트는 사용자의 새로운 명시적 요청 없이 재시도하지 않는다.

예상 기본 주소: https://YunSangYeong.github.io/Craftsman-Nail-Technician-CBT/
이 주소는 배포 성공·실제 공개 확인을 뜻하지 않는다.

## 재사용 환경 설정

이번 클라우드 환경 초안에는 `install_script`와 `start_skill`을 저장했다.
설치 명령과 개발 서버 시작/로컬 요청·검사 명령, 현재 배포 중단 상태를 담았다.
환경 설정에서 검토·저장 후 환경 Publish가 필요하며, 이는 GitHub Pages 게시와 별개다.
초안 저장은 환경 게시나 새 작업에서의 복원 검증이 아니다.
