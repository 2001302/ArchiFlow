"""
설정 관리 모듈
API 키와 서버 설정을 관리합니다.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # AI API Keys
    perplexity_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Server Configuration
    host: str = "localhost"
    port: int = 8000
    debug: bool = True
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/ai_engine.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# 전역 설정 인스턴스
settings = Settings()

# API 키 검증
def validate_api_keys() -> dict:
    """API 키 유효성 검사"""
    missing_keys = []
    
    if not settings.perplexity_api_key:
        missing_keys.append("PERPLEXITY_API_KEY")
    if not settings.openai_api_key:
        missing_keys.append("OPENAI_API_KEY")
    if not settings.anthropic_api_key:
        missing_keys.append("ANTHROPIC_API_KEY")
    
    return {
        "valid": len(missing_keys) == 0,
        "missing_keys": missing_keys
    }
