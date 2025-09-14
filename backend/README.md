# AI 엔진 백엔드

옵시디언 플러그인용 AI 엔진 백엔드 서버입니다.

## 기능

- **다중 AI 제공자 지원**: Perplexity, OpenAI, Anthropic
- **다양한 출력 형식**: 텍스트, 문서
- **RESTful API**: FastAPI 기반
- **비동기 처리**: 고성능 비동기 처리
- **로깅**: 상세한 로깅 및 모니터링
- **테스트**: 포괄적인 유닛테스트

## 설치

### 1. 의존성 설치

```bash
pip3 install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 API 키를 설정합니다:

```env
PERPLEXITY_API_KEY=your_perplexity_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 3. 설정 파일 구성

`config.json` 파일을 편집하여 모델과 제공자를 설정합니다:

```json
{
  "name": "My Model",
  "version": "1.0.0",
  "providers": {
    "perplexity": {
      "api_url": "https://api.perplexity.ai",
      "auth_header": "Authorization",
      "auth_prefix": "Bearer"
    },
    "openai": {
      "api_url": "https://api.openai.com/v1/chat/completions",
      "auth_header": "Authorization",
      "auth_prefix": "Bearer"
    },
    "anthropic": {
      "api_url": "https://api.anthropic.com/v1/messages",
      "auth_header": "x-api-key",
      "auth_prefix": ""
    }
  },
  "models": [
    {
      "name": "perplexity",
      "provider": "perplexity",
      "model": "sonar-pro",
      "api_key": "your_api_key"
    }
  ]
}
```

## 실행

### 개발 환경

```bash
python3 main.py
```

### 프로덕션 환경

```bash
# PyInstaller로 빌드된 실행파일 실행
./dist/documize-backend
```

## API 엔드포인트

### 1. 헬스 체크

```http
GET /health
```

**응답:**
```json
{
  "status": "healthy",
  "api_keys_valid": true,
  "missing_keys": []
}
```

### 2. AI 응답 생성

```http
POST /generate
Content-Type: application/json

{
  "prompt": "사용자 프롬프트",
  "output_format": "text",
  "provider": "perplexity",
  "model": "sonar-pro",
  "api_key": "your_api_key",
  "language": "python"
}
```

**응답:**
```json
{
  "success": true,
  "content": "AI 응답 내용",
  "format": "text",
  "provider": "perplexity"
}
```

### 3. 지원 형식 조회

```http
GET /formats
```

**응답:**
```json
{
  "formats": ["text", "document"],
  "providers": ["perplexity", "openai", "anthropic"]
}
```

## 테스트

### 전체 테스트 실행

```bash
python3 run_tests.py
```

### 특정 테스트 실행

```bash
python3 run_tests.py test_ai_engine.py
```

### 커버리지 포함 테스트

```bash
python3 -m pytest tests/ --cov=ai_core --cov=documize_api --cov-report=html
```

### 테스트 구조

```
tests/
├── conftest.py              # 테스트 설정 및 픽스처
├── test_ai_engine.py        # AI 엔진 테스트
├── test_api_server.py       # API 서버 테스트
├── test_providers.py        # AI 제공자 테스트
├── test_prompt_manager.py   # 프롬프트 매니저 테스트
├── test_response_processor.py # 응답 후처리 테스트
└── test_utils.py            # 유틸리티 테스트
```

## 빌드

### PyInstaller로 실행파일 생성

```bash
python3 build_backend.py
```

### 빌드된 파일 위치

```
dist/
└── documize-backend
```

## 로깅

로그 파일은 `logs/ai_engine.log`에 저장됩니다.

### 로그 레벨 설정

환경 변수 `LOG_LEVEL`을 설정하여 로그 레벨을 조정할 수 있습니다:

```env
LOG_LEVEL=DEBUG
```

## 문제 해결

### 1. 백엔드가 시작되지 않는 경우

- API 키가 올바르게 설정되었는지 확인
- 포트 8000이 사용 중이지 않은지 확인
- 의존성이 올바르게 설치되었는지 확인

### 2. AI 요청이 실패하는 경우

- API 키가 유효한지 확인
- 네트워크 연결 상태 확인
- 모델명이 올바른지 확인

### 3. 테스트가 실패하는 경우

- 모든 의존성이 설치되었는지 확인
- Python 버전이 3.8 이상인지 확인
- 가상환경이 활성화되었는지 확인

## 개발

### 코드 스타일

- PEP 8 스타일 가이드 준수
- 타입 힌트 사용
- 독스트링 작성

### 테스트 작성

- 모든 새로운 기능에 대한 테스트 작성
- 커버리지 80% 이상 유지
- Mock을 사용한 단위 테스트

### 기여

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 라이선스

MIT License

## 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.
