
## 프로젝트 구조

```
backend/
├── main.py                          # 메인 실행 파일
├── start.sh                         # 서버 시작 스크립트
├── requirements.txt                 # Python 의존성
├── venv/                           # Python 가상환경
├── mcp_server/                     # MCP (Model Context Protocol) 서버
│   ├── config/
│   │   └── settings.py             # AI Core 설정 관리
│   ├── managers/
│   │   ├── mcp_engine.py          # MCP 엔진 핵심 로직
│   │   ├── prompt_manager.py      # 프롬프트 관리
│   │   └── provider_manager.py    # AI 제공자 관리
│   ├── models/
│   │   ├── enums.py               # 열거형 정의
│   │   └── schemas.py             # 데이터 스키마
│   ├── providers/                 # AI 제공자 구현
│   │   ├── base_provider.py       # 기본 제공자 인터페이스
│   │   ├── openai_provider.py     # OpenAI 제공자
│   │   ├── anthropic_provider.py  # Anthropic 제공자
│   │   └── perplexity_provider.py # Perplexity 제공자
│   ├── processors/
│   │   └── response_processor.py  # 응답 처리
│   ├── mcp_tool/                  # MCP 도구
│   │   └── tools/
│   │       ├── ai_generation.py   # AI 생성 도구
│   │       ├── content_management.py # 콘텐츠 관리 도구
│   │       └── vault_operations.py # 볼트 작업 도구
│   └── utils/                     # 유틸리티
│       ├── decorators.py          # 데코레이터
│       ├── logging.py             # 로깅 유틸리티
│       ├── response_formatter.py  # 응답 포맷터
│       └── validation.py          # 유효성 검사
├── mcp_obsidian/                  # 옵시디언 특화 MCP 구현
│   ├── config/
│   │   └── obsidian_settings.py   # 옵시디언 설정 관리
│   ├── managers/
│   │   └── obsidian_engine.py     # 옵시디언 엔진
│   ├── tools/
│   │   ├── note_processor.py      # 노트 처리 도구
│   │   └── vault_manager.py       # 볼트 관리 도구
│   └── models/                    # 옵시디언 모델
└── documize_api/                  # FastAPI 애플리케이션
    ├── main.py                    # FastAPI 서버 메인 로직
    ├── config/                    # API 설정
    ├── middleware/                # 미들웨어
    ├── routes/                    # API 라우트
    └── services/                  # 비즈니스 로직
```

## �� 주요 기능

### 1. AI 엔진 통합
- **다중 AI 제공자 지원**: OpenAI, Anthropic, Perplexity
- **유연한 출력 형식**: 텍스트, 문서, 코드 등
- **프롬프트 관리**: 체계적인 프롬프트 템플릿 관리

### 2. 옵시디언 통합
- **볼트 관리**: 노트 생성, 읽기, 수정, 삭제
- **검색 기능**: 콘텐츠 및 메타데이터 검색
- **AI 기반 노트 처리**: 자동 요약, 태깅, 링크 제안

### 3. MCP (Model Context Protocol) 지원
- **도구 기반 AI**: AI가 직접 볼트를 조작할 수 있는 도구 제공
- **확장 가능한 아키텍처**: 새로운 도구와 기능 쉽게 추가
