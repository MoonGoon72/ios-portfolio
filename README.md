# 문영균 iOS 포트폴리오

[웹 포트폴리오](https://moongoon72.github.io/ios-portfolio/)

반응형 웹과 다운로드용 PDF를 같은 내용으로 관리합니다. 웹에서는 상세 경험을 펼쳐 읽고, PDF에는 전체 사례를 담습니다.

## 수정

- 내용: `content.json`
- 화면 구성: `build.py`
- 디자인: `dist/style.css`
- 이미지와 글꼴: `dist/assets/`
- 생성된 제출 문안: `portfolio-copy.md`

`python3 build.py`로 HTML과 문안을 생성합니다. `main`에 푸시하면 GitHub Actions가 웹을 생성하고 PC·태블릿·모바일 레이아웃을 확인한 뒤 PDF를 다시 출력해 GitHub Pages에 게시합니다.

로컬 PDF 생성 및 검증:

```sh
npm ci
npx playwright install chromium
python3 build.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory dist
# 다른 터미널에서
npm run verify
```

## 이미지와 기여

격투 게임 정보 앱의 탐색·목록·검색·영상·메모 화면은 직접 제공한 개발 화면입니다. 토닥운은 팀에서 제작한 소개 이미지를 사용합니다. 레츠톡은 프로젝트 README에 보존된 당시 화면을 사용합니다. 화면만으로 현재 배포 상태를 뜻하지 않으며 프로젝트별 상태와 담당 범위는 본문에 표시합니다.

글꼴은 Pretendard이며 SIL Open Font License를 `dist/assets/OFL.txt`에 포함합니다.
