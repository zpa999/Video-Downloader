# 🎬 유튜브 다운로더 (YouTube Downloader)

PyQt5와 yt-dlp를 기반으로 제작된 직관적이고 깔끔한 데스크톱 유튜브 동영상 다운로더 프로그램입니다.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?logo=qt)
![yt-dlp](https://img.shields.io/badge/Engine-yt--dlp-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ✨ 주요 기능

* 🔗 **간편한 다운로드**: 유튜브 영상 URL 입력 후 클릭 한 번으로 최고 화질 영상 다운로드
* 📊 **실시간 다운로드 상태 안내**:
  * 실시간 진행률(%) 프로그레스 바
  * 현재 다운로드 속도 및 예상 잔여 시간(ETA) 표시
* ⚡ **안정적인 백그라운드 처리**: `QThread`를 활용하여 대용량 다운로드 중에도 UI가 멈추지 않는 비동기 처리
* 🛡️ **유튜브 403 Forbidden 차단 우회**: 최신 유튜브 보안 정책에 대응하여 모바일 클라이언트(`android`, `ios`) 프로토콜을 활용한 다운로드 지원
* 🪟 **윈도우 전용 설치 프로그램 제공**: Inno Setup 기반의 손쉬운 원클릭 설치 및 바로가기 생성

---

## 🛠️ 기술 스택

| 분류 | 기술 |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **GUI Framework** | PyQt5 |
| **Download Engine** | yt-dlp |
| **Packaging / Build** | PyInstaller |
| **Installer Compiler** | Inno Setup 6 |

---

## 🚀 시작하기

### 1. 사전 요구사항
* [Python 3.10](https://www.python.org/) 이상
* ffmpeg는 `imageio-ffmpeg`로 자동 포함되므로 별도 설치가 필요 없습니다

### 2. 패키지 설치
```bash
pip install PyQt5 yt-dlp
```

### 3. 프로그램 실행
```bash
python main.py
```

---

## 📦 빌드 및 패키징

### 1) PyInstaller 실행 파일 빌드
```bash
pyinstaller --clean YoutubeDownloader.spec
```
빌드가 완료되면 `dist/YoutubeDownloader/` 폴더에 실행에 필요한 파일들이 생성됩니다.

### 2) Inno Setup 설치 프로그램(Setup Installer) 컴파일
`Inno Setup 6`가 설치된 상태에서 스크립트를 컴파일합니다:
```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```
컴파일 완료 시 `Output/` 폴더에 `유튜브다운로더_Setup_v1.0.3.exe` 파일이 생성됩니다.

---

## 📁 프로젝트 구조

```text
myproject/
├── Output/                      # Inno Setup으로 생성된 최종 윈도우 설치 파일 (.exe)
│   └── 유튜브다운로더_Setup_v1.0.3.exe
├── dist/                        # PyInstaller 빌드 결과물
├── main.py                      # 메인 소스 코드 (PyQt5 GUI 및 다운로드 로직)
├── setup.iss                    # Inno Setup 패키징 스크립트
├── YoutubeDownloader.spec       # PyInstaller 빌드 명세서
└── README.md                    # 프로젝트 안내 문서
```

---

## 📝 릴리즈 노트

* **v1.0.3 (2026-10-13)**
  * 다운로드 포맷을 호환성 높은 mp4(H.264 + AAC)로 변경 (기존 webm 출력 개선)
  * 병합 결과 컨테이너를 mp4로 고정(`merge_output_format`)
* **v1.0.2 (2026-10-13)**
  * 유튜브 `HTTP Error 403: Forbidden` 근본 해결: PO Token이 필요한 `android`/`ios` 클라이언트 강제 지정 제거
  * yt-dlp 2026.8.19로 업데이트 및 JS 런타임(deno/node) 지정
  * 영상+음원 분리 제공 방식에 대응(`bv*+ba/b`), ffmpeg(`imageio-ffmpeg`) 내장으로 별도 설치 불필요
  * 다운로드 재시도(`retries`) 옵션 추가
* **v1.0.1 (2026-09-30)**
  * 유튜브 `HTTP Error 403: Forbidden` 차단 우회 옵션(`extractor_args`) 추가
  * 파일명 특수문자 호환성 옵션(`windowsfilenames`) 추가
  * 최신 엔진 기반 설치 파일(`유튜브다운로더_Setup_v1.0.1.exe`) 배포
* **v1.0.0 (2026-06-11)**
  * 초기 버전 출시 (PyQt5 GUI 인터페이스 및 기본 다운로드 기능)
