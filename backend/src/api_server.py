"""
FastAPI 기반 백그라운드 서버
옵시디언 플러그인과 통신하는 API 서버입니다.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger
import uvicorn

from .ai_engine import AIEngine, OutputFormat, AIProvider
from .config import settings, validate_api_keys

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

# AI 엔진 인스턴스
ai_engine = AIEngine()

# 요청/응답 모델
class AIRequest(BaseModel):
    """AI 요청 모델"""
    prompt: str
    output_format: str  # "mermaid", "source_code", "text"
    provider: str = "perplexity"  # "perplexity", "openai", "anthropic"
    api_key: Optional[str] = None  # 클라이언트에서 전달받은 API Key
    source_code: Optional[str] = None
    diagram_context: Optional[str] = None

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
    """헬스 체크 엔드포인트"""
    api_validation = validate_api_keys()
    return HealthResponse(
        status="healthy" if api_validation["valid"] else "unhealthy",
        api_keys_valid=api_validation["valid"],
        missing_keys=api_validation["missing_keys"]
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
        
        # AI 응답 생성
        result = await ai_engine.generate_response(
            prompt=request.prompt,
            output_format=output_format,
            provider=provider,
            api_key=request.api_key,
            source_code=request.source_code,
            diagram_context=request.diagram_context
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


def run_server():
    """서버 실행"""
    # 로그 설정
    logger.add(
        settings.log_file,
        level=settings.log_level,
        rotation="1 day",
        retention="7 days"
    )
    
    logger.info("AI 엔진 서버 시작")
    
    # 서버 실행
    uvicorn.run(
        "src.api_server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

if __name__ == "__main__":
    run_server()
