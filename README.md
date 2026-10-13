# 문영균 iOS 포트폴리오

[웹 포트폴리오](https://moongoon72.github.io/ios-portfolio/)

반응형 웹과 다운로드용 PDF를 같은 내용으로 관리합니다. 웹에서는 상세 경험을 펼쳐 읽고, PDF에는 전체 사례를 담습니다.

## 수정

- 내용: `content.json`
- 화면 구성: `build.py`
- 디자인: `dist/style.css`
- 이미지와 글꼴: `dist/assets/`
- 생성된 제출 문안: `portfolio-copy.md`

`python3 build.py`로 HTML과 문안을 생성합니다. `main`에 푸시하면 GitHub Actions가 웹을 생성해 GitHub Pages에 게시합니다.

로컬 미리보기:

```sh
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
```

기본 브라우저 Aside에서 `http://127.0.0.1:8765/`를 열어 화면을 확인합니다. PDF는 브라우저 인쇄에서 PDF로 저장한 뒤 `dist/portfolio.pdf`를 교체합니다. 배포에서는 저장된 PDF를 그대로 게시합니다.

## 이미지와 기여

격투 게임 정보 앱의 탐색·목록·검색·영상·메모 화면은 직접 제공한 개발 화면입니다. 토닥운은 팀에서 제작한 소개 이미지를 사용합니다. 레츠톡은 프로젝트 README에 보존된 당시 화면을 사용합니다. 화면만으로 현재 배포 상태를 뜻하지 않으며 프로젝트별 상태와 담당 범위는 본문에 표시합니다.

글꼴은 Pretendard이며 SIL Open Font License를 `dist/assets/OFL.txt`에 포함합니다.

## 이력서에서 사례로 바로 연결

영어 지원 상세: https://moongoon72.github.io/ios-portfolio/#tk8-localization

직접 연결하면 해당 상세가 자동으로 펼쳐집니다. 기존 프로젝트 링크 `#tk8`도 유지합니다.

## 2026-10-13 이력서 기준 개편

최신 이력서의 4개 프로젝트·9개 대표 경험을 상세화합니다.

- 영어 지원: `#tk8-localization`
- 데이터 캐싱: `#tk8-data-cache`
- 이미지 캐싱·전송량 관리: `#tk8-image-cache`
- 책임·의존성 분리: `#tk8-responsibility`
- SSE 응답: `#todakun-sse`
- 사전 검토 스킬: `#todakun-preflight`
- CloudKit 목록 갱신: `#retstalk-cloudkit`
- 고객지원 도구: `#intern-support`
- Electron PoC: `#intern-electron`

각 주소로 진입하면 해당 사례를 자동으로 펼칩니다.
