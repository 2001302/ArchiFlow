# ArchiFlow Plugin

옵시디언용 ArchiFlow 플러그인입니다.

## 프로젝트 구조

```
obsidian-sample-plugin/
├── manifest.json          # 옵시디언 플러그인 메타데이터
├── main.js               # 컴파일된 메인 파일 (옵시디언이 인식)
├── styles.css            # 스타일시트 (옵시디언이 인식)
├── package.json          # 루트 빌드 스크립트
├── frontend/             # 프론트엔드 (TypeScript/JavaScript)
│   ├── main.ts           # TypeScript 메인 파일
│   ├── src/              # TypeScript 소스 코드
│   ├── package.json      # 프론트엔드 의존성
│   ├── tsconfig.json     # TypeScript 설정
│   ├── esbuild.config.mjs # 빌드 설정
│   └── node_modules/     # 프론트엔드 의존성 패키지
├── backend/              # 백엔드 (Python)
│   ├── main.py           # Python 메인 파일
│   ├── src/              # Python 소스 코드
│   ├── requirements.txt  # Python 의존성
│   └── venv/             # Python 가상환경
└── docs/                 # 문서
```

## 개발 방법

### 프론트엔드 개발
```bash
# 개발 모드 (자동 재빌드)
npm run dev

# 프로덕션 빌드
npm run build
```

### 백엔드 개발
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 빌드

### 프론트엔드 빌드
```bash
npm run build
```
이 명령어는 frontend 폴더에서 TypeScript를 컴파일하고 루트에 main.js를 생성합니다.

### 백엔드 실행파일 빌드
```bash
# Windows
build_backend.bat

# macOS/Linux
./build_backend.sh

# 또는 직접 Python 스크립트 실행
python build_backend.py
```

이 명령어는 PyInstaller를 사용하여 backend를 단일 실행파일로 빌드합니다.
빌드된 실행파일은 `dist/documize-backend` (또는 Windows에서는 `dist/documize-backend.exe`)에 생성됩니다.

## 실행

플러그인이 로드되면 자동으로 backend 실행파일이 시작됩니다. 
- Backend 서버는 `http://localhost:8000`에서 실행됩니다.
- Frontend는 자동으로 backend 서버에 연결됩니다.
- 플러그인이 비활성화되면 backend 서버도 자동으로 종료됩니다.

## 요구사항

- Node.js (프론트엔드 빌드용)
- Python 3.8+ (백엔드용)
- PyInstaller (백엔드 실행파일 빌드용)
