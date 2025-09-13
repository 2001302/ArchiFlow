"""
FastAPI 기반 백그라운드 서버
옵시디언 플러그인과 통신하는 API 서버입니다.
"""
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger
import uvicorn

# PyInstaller 환경을 위한 import 처리
import sys
import os
from pathlib import Path

# PyInstaller 환경에서의 모듈 경로 처리
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행파일인 경우
    current_dir = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(os.path.dirname(sys.executable))
    src_path = current_dir / "src"
    sys.path.insert(0, str(src_path))

# 절대 import 사용 - 모든 환경에서 동일하게 동작
from ai_engine import AIEngine
from enums import OutputFormat
from ai_providers import AIProvider
from config import settings, validate_api_keys

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

# AI 엔진 인스턴스 - 지연 로딩
ai_engine = None

def get_ai_engine():
    """AI 엔진 인스턴스를 지연 로딩으로 가져오기"""
    global ai_engine
    if ai_engine is None:
        ai_engine = AIEngine()
    return ai_engine

# 요청/응답 모델
class AIRequest(BaseModel):
    """AI 요청 모델"""
    prompt: str
    output_format: str  # "text", "document"
    provider: str = "perplexity"  # "perplexity", "openai", "anthropic"
    model: str = "gpt-4"  # 모델명
    api_key: Optional[str] = None  # 클라이언트에서 전달받은 API Key
    language: Optional[str] = None  # 프로그래밍 언어

class ConnectionTestRequest(BaseModel):
    """연결 테스트 요청 모델"""
    provider: str  # "perplexity", "openai", "anthropic"
    api_key: str

class AIResponse(BaseModel):
    """AI 응답 모델"""
    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    format: Optional[str] = None
    provider: Optional[str] = None

class HealthResponse(BaseModel):
    """헬스 체크 응답 모델"""
    status: str
    api_keys_valid: bool
    missing_keys: list

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
        # 출력 형식 검증
        try:
            output_format = OutputFormat(request.output_format)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 출력 형식입니다: {request.output_format}"
            )
        
        # AI 제공자 검증
        try:
            provider = AIProvider(request.provider)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 AI 제공자입니다: {request.provider}"
            )
        
        # AI 응답 생성 - 지연 로딩
        engine = get_ai_engine()
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

@app.post("/test-connection")
async def test_connection(request: ConnectionTestRequest):
    """API 연결 테스트 엔드포인트"""
    try:
        # AI 제공자 검증
        try:
            provider = AIProvider(request.provider)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"지원하지 않는 AI 제공자입니다: {request.provider}"
            )
        
        # API Key가 제공되었는지 확인
        if not request.api_key:
            raise HTTPException(
                status_code=400,
                detail="API Key가 제공되지 않았습니다."
            )
        
        # 간단한 테스트 요청으로 연결 확인 - 지연 로딩
        engine = get_ai_engine()
        test_result = await engine.test_connection(
            provider=provider,
            api_key=request.api_key
        )
        
        return {
            "success": test_result["success"],
            "message": test_result["message"],
            "provider": request.provider
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"연결 테스트 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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
        app_module = "api_server:app"
    else:
        # 개발 환경인 경우
        app_module = "src.api_server:app"
    
    # 서버 실행 - 더 빠른 시작을 위한 설정
    uvicorn.run(
        app_module,
        host=settings.host,
        port=settings.port,
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
