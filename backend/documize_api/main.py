"""
FastAPI 기반 백그라운드 서버
옵시디언 플러그인과 통신하는 API 서버입니다.
"""
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from loguru import logger
import uvicorn

# PyInstaller 환경을 위한 import 처리
import os
from pathlib import Path

# PyInstaller 환경에서의 모듈 경로 처리
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행파일인 경우
    current_dir = Path(getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)))
    src_path = current_dir / "src"
    sys.path.insert(0, str(src_path))

# MCP Server 모듈 경로 추가
mcp_server_path = Path(__file__).parent.parent / "mcp_server"
sys.path.insert(0, str(mcp_server_path))

from mcp_server import MCPEngine, AIProvider, OutputFormat
from mcp_server.models.schemas import AIRequest, AIResponse, HealthResponse
from mcp_server.config.settings import settings, validate_api_keys
# MCP 서버는 더 이상 사용하지 않음

# FastAPI 앱 생성
app = FastAPI(
    title="Obsidian AI Engine",
    description="옵시디언 플러그인용 AI 엔진 백엔드",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서만 사용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MCP 엔진 인스턴스 - 지연 로딩
mcp_engine = None

def get_mcp_engine():
    """MCP 엔진 인스턴스를 지연 로딩으로 가져오기"""
    global mcp_engine
    if mcp_engine is None:
        mcp_engine = MCPEngine()
    return mcp_engine

# MCP 서버는 더 이상 사용하지 않음

@app.get("/", response_model=Dict[str, str])
async def root():
    """루트 엔드포인트"""
    return {"message": "Obsidian AI Engine Backend is running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """헬스 체크 엔드포인트 - 빠른 응답을 위한 최적화"""
    try:
        # 서버가 실행 중임을 즉시 알림 (API 키 검증은 생략하여 빠른 응답)
        return HealthResponse(
            status="healthy",  # 서버가 실행 중이면 항상 healthy
            api_keys_valid=True,  # 헬스 체크에서는 API 키 검증 생략
            missing_keys=[]  # 빈 리스트로 설정
        )
    except Exception as e:
        logger.error(f"헬스 체크 중 오류: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            api_keys_valid=False,
            missing_keys=["UNKNOWN_ERROR"]
        )

@app.post("/generate", response_model=AIResponse)
async def generate_ai_response(request: AIRequest):
    """AI 응답 생성 엔드포인트"""
    try:
        try:
            output_format = OutputFormat(request.output_format)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 출력 형식입니다: {request.output_format}"
            )
        
        try:
            provider = AIProvider(request.provider)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 AI 제공자입니다: {request.provider}"
            )
        
        engine = get_mcp_engine()
        result = await engine.generate_response(
            prompt=request.prompt,
            output_format=output_format,
            provider=provider,
            model=request.model,
            api_key=request.api_key,
            language=request.language
        )
        
        return AIResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI 응답 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/formats")
async def get_supported_formats():
    """지원하는 출력 형식 목록"""
    return {
        "formats": [format.value for format in OutputFormat],
        "providers": [provider.value for provider in AIProvider]
    }

@app.get("/api/info")
async def get_api_info():
    """API 정보 및 사용 가능한 엔드포인트 목록"""
    return {
        "ai_modes": {
            "current": settings.ai_request_mode,
            "available": ["direct", "mcp"]
        },
        "endpoints": {
            "basic_ai": {
                "url": "/ai/basic/generate",
                "description": "기본 AI 텍스트 생성 - 간단한 질문/답변",
                "method": "POST",
                "use_case": "일반적인 텍스트 생성, 질문 답변"
            },
            "advanced_ai": {
                "url": "/ai/advanced/generate", 
                "description": "고급 AI 문서 생성 - 구조화된 코드/문서",
                "method": "POST",
                "use_case": "코드 생성, 구조화된 문서 작성"
            },
            "legacy_generate": {
                "url": "/generate",
                "description": "레거시 AI 생성 - 설정에 따라 direct/mcp 모드",
                "method": "POST",
                "use_case": "기존 호환성을 위한 엔드포인트"
            },
            "mcp_tools": {
                "url": "/mcp/tools/call",
                "description": "MCP 도구 직접 호출 - 볼트 조작, 콘텐츠 관리",
                "method": "POST",
                "use_case": "파일 조작, 검색, 메타데이터 관리"
            }
        },
        "recommendations": {
            "frontend_usage": {
                "basic_ai": "사용자가 간단한 질문을 할 때 사용",
                "advanced_ai": "코드 생성이나 구조화된 문서가 필요할 때 사용",
                "mcp_tools": "볼트 파일 조작이나 고급 기능이 필요할 때 사용"
            }
        }
    }

@app.get("/config/ai-mode")
async def get_ai_mode():
    """현재 AI 요청 모드 조회"""
    return {
        "ai_request_mode": settings.ai_request_mode,
        "available_modes": ["direct", "mcp"],
        "description": {
            "direct": "AI 엔진을 직접 호출하는 방식",
            "mcp": "MCP 서버를 통한 통합 처리 방식"
        }
    }

@app.post("/config/ai-mode")
async def set_ai_mode(mode: str):
    """AI 요청 모드 변경"""
    if mode not in ["direct", "mcp"]:
        raise HTTPException(
            status_code=400,
            detail="지원하지 않는 AI 모드입니다. 'direct' 또는 'mcp'를 사용하세요."
        )
    
    # 설정 업데이트 (런타임에서만 적용)
    settings.ai_request_mode = mode
    logger.info(f"AI 요청 모드가 {mode}로 변경되었습니다.")
    
    return {
        "message": f"AI 요청 모드가 {mode}로 변경되었습니다.",
        "ai_request_mode": mode
    }

# 기본 AI 요청과 고급 기능을 구분하는 엔드포인트들
@app.post("/ai/basic/generate")
async def basic_ai_generate(request: AIRequest):
    """기본 AI 생성 요청 - 간단한 텍스트 생성"""
    try:
        # 기본 요청은 항상 텍스트 형식으로 처리
        basic_request = AIRequest(
            prompt=request.prompt,
            output_format="text",
            provider=request.provider,
            model=request.model,
            api_key=request.api_key,
            language=None  # 기본 요청에서는 언어 무시
        )
        
        # MCP 엔진을 통한 처리
        engine = get_mcp_engine()
        result = await engine.generate_response(
            prompt=basic_request.prompt,
            output_format=OutputFormat.TEXT,
            provider=AIProvider(basic_request.provider),
            model=basic_request.model,
            api_key=basic_request.api_key
        )
        
        return AIResponse(**result)
            
    except Exception as e:
        logger.error(f"기본 AI 생성 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ai/advanced/generate")
async def advanced_ai_generate(request: AIRequest):
    """고급 AI 생성 요청 - 구조화된 문서 생성"""
    try:
        # 고급 요청은 문서 형식으로 처리
        advanced_request = AIRequest(
            prompt=request.prompt,
            output_format="document",
            provider=request.provider,
            model=request.model,
            api_key=request.api_key,
            language=request.language or "python"
        )
        
        # MCP 엔진을 통한 처리
        engine = get_mcp_engine()
        result = await engine.generate_response(
            prompt=advanced_request.prompt,
            output_format=OutputFormat.DOCUMENT,
            provider=AIProvider(advanced_request.provider),
            model=advanced_request.model,
            api_key=advanced_request.api_key,
            language=advanced_request.language
        )
        
        return AIResponse(**result)
            
    except Exception as e:
        logger.error(f"고급 AI 생성 중 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# MCP 도구들과 볼트 조작 API는 별도 모듈로 분리됨

def run_server():
    """서버 실행"""
    import os
    from pathlib import Path
    
    # 로그 디렉토리 생성
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 로그 설정
    logger.add(
        settings.log_file,
        level=settings.log_level,
        rotation="1 day",
        retention="7 days"
    )
    
    logger.info("AI 엔진 서버 시작")
    
    # PyInstaller 환경에서의 모듈 경로 처리
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 실행파일인 경우
        app_module = "documize_api.main:app"
    else:
        # 개발 환경인 경우
        app_module = "documize_api.main:app"
    
    # 서버 실행 - 더 빠른 시작을 위한 설정
    uvicorn.run(
        app_module,
        host="localhost",
        port=8000,
        reload=False,  # PyInstaller에서는 reload를 비활성화
        log_level="warning",  # 로그 레벨을 warning으로 설정하여 시작 속도 향상
        access_log=False,  # 액세스 로그 비활성화로 시작 속도 향상
        server_header=False,  # 서버 헤더 비활성화
        date_header=False,  # 날짜 헤더 비활성화
        loop="asyncio",  # 명시적으로 asyncio 루프 사용
        workers=1,  # 단일 워커로 설정
        limit_concurrency=100,  # 동시 연결 제한
        limit_max_requests=1000,  # 최대 요청 수 제한
        timeout_keep_alive=5  # keep-alive 타임아웃 설정
    )

if __name__ == "__main__":
    run_server()
