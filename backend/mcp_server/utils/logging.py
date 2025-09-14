"""
로깅 유틸리티
"""
from loguru import logger

def log_api_call(
    provider: str, 
    success: bool, 
    duration: float, 
    prompt_length: int = 0
) -> None:
    """
    API 호출 로깅
    
    Args:
        provider: AI 제공자
        success: 성공 여부
        duration: 소요 시간 (초)
        prompt_length: 프롬프트 길이
    """
    status = "SUCCESS" if success else "FAILED"
    logger.info(
        f"API Call - Provider: {provider}, Status: {status}, "
        f"Duration: {duration:.2f}s, Prompt Length: {prompt_length}"
    )

def setup_logger(log_file: str, log_level: str = "INFO"):
    """
    로거 설정
    
    Args:
        log_file: 로그 파일 경로
        log_level: 로그 레벨
    """
    logger.add(
        log_file,
        level=log_level,
        rotation="1 day",
        retention="7 days"
    )
