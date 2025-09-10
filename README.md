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

플러그인을 빌드하려면:
```bash
npm run build
```

이 명령어는 frontend 폴더에서 TypeScript를 컴파일하고 루트에 main.js를 생성합니다.
