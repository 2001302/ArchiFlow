"""
Pydantic 모델 정의
"""
from pydantic import BaseModel
from typing import Optional

class AIRequest(BaseModel):
    """AI 요청 모델"""
    prompt: str
    output_format: str  # "text", "document"
    provider: str = "perplexity"  # "perplexity", "openai", "anthropic"
    model: str = "gpt-4"  # 모델명
    api_key: Optional[str] = None  # 클라이언트에서 전달받은 API Key
    language: Optional[str] = None  # 프로그래밍 언어

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
