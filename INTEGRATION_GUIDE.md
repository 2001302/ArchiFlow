# 백엔드 구조 가이드

## 개요

AI Core와 REST API를 통합하여 하나의 실행 파일로 제공합니다.

## 구조 변경사항

### 현재 구조
```
├── backend/
│   ├── main.py (FastAPI 서버)
│   └── mcp_server/ (AI Core 라이브러리)
│       ├── managers/ (MCP 엔진 포함)
│       └── mcp_tool/ (MCP 도구들)
├── build_backend.py
└── build_integrated.py
```

## 주요 개선사항

### 1. 단일 실행 파일
- 하나의 실행 파일로 모든 기능 제공
- 리소스 효율성 향상
- 배포 및 관리 간소화

### 2. 통합 API 엔드포인트
- REST API와 MCP 기능을 하나의 서버에서 제공
- 포트 8000에서 모든 기능 접근 가능

### 3. 기능 통합
- AI 생성 기능 (기존 `/generate`)
- 볼트 조작 기능 (새로운 `/vault/*` 엔드포인트)
- MCP 도구 호출 (새로운 `/mcp/*` 엔드포인트)

## API 엔드포인트

### 기존 엔드포인트
- `POST /generate` - AI 응답 생성
- `GET /health` - 헬스 체크
- `GET /formats` - 지원 형식 목록

### 새로운 엔드포인트

#### 볼트 조작
- `GET /vault/files` - 볼트 파일 목록 조회
- `GET /vault/files/{file_path}` - 파일 내용 읽기
- `POST /vault/notes` - 새 노트 생성
- `PUT /vault/notes/{file_path}` - 노트 업데이트
- `GET /vault/search` - 볼트 내 검색

#### MCP 도구
- `POST /mcp/tools/list` - MCP 도구 목록 조회
- `POST /mcp/tools/call` - MCP 도구 호출

## 빌드 및 실행

### 통합 빌드
```bash
python3 build_integrated.py
```

### 실행
```bash
./dist/documize-integrated
```

### 개발 환경에서 실행
```bash
cd backend
python3 main.py
```

## 장점

1. **단순화된 아키텍처**: 하나의 서버로 모든 기능 제공
2. **리소스 효율성**: 중복된 의존성과 프로세스 제거
3. **관리 편의성**: 하나의 실행 파일만 관리
4. **API 통합**: REST API와 MCP 기능을 통합된 인터페이스로 제공
5. **확장성**: 새로운 기능을 쉽게 추가 가능

## 마이그레이션 가이드

### 기존 사용자
1. 기존 분리된 실행 파일 대신 통합 실행 파일 사용
2. MCP 기능이 필요한 경우 `/mcp/*` 엔드포인트 사용
3. 볼트 조작이 필요한 경우 `/vault/*` 엔드포인트 사용

### 개발자
1. `build_integrated.py` 사용하여 빌드
2. 새로운 기능 추가 시 `documize_api/main.py`에 엔드포인트 추가
3. MCP 도구 추가 시 `mcp_server/mcp_server/tools/`에 구현

## 문제 해결

### 빌드 오류
- 가상환경이 활성화되어 있는지 확인
- 모든 의존성이 설치되어 있는지 확인
- `requirements.txt` 업데이트 후 재설치

### 실행 오류
- 포트 8000이 사용 중인지 확인
- 볼트 경로가 올바른지 확인
- API 키가 설정되어 있는지 확인

## 향후 계획

1. **웹 인터페이스**: 통합된 웹 UI 제공
2. **설정 관리**: 통합된 설정 시스템
3. **모니터링**: 통합된 로깅 및 모니터링
4. **플러그인 시스템**: 확장 가능한 플러그인 아키텍처
