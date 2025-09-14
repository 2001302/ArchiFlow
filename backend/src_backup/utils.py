"""
유틸리티 모듈
공통 유틸리티 함수들을 제공합니다.
"""
import asyncio
from typing import Dict, Any, Optional
import time
from loguru import logger

def validate_api_key(api_key: Optional[str]) -> bool:
    """
    API 키 유효성 검사
    
    Args:
        api_key: API 키
    
    Returns:
        유효성 여부
    """
    return api_key is not None and len(api_key.strip()) > 0

def format_error_response(error: str, provider: str = "unknown") -> Dict[str, Any]:
    """
    에러 응답 포맷팅
    
    Args:
        error: 에러 메시지
        provider: AI 제공자
    
    Returns:
        포맷된 에러 응답
    """
    return {
        "success": False,
        "error": error,
        "content": None,
        "provider": provider
    }

def format_success_response(
    content: str, 
    output_format: str, 
    provider: str
) -> Dict[str, Any]:
    """
    성공 응답 포맷팅
    
    Args:
        content: 응답 내용
        output_format: 출력 형식
        provider: AI 제공자
    
    Returns:
        포맷된 성공 응답
    """
    return {
        "success": True,
        "content": content,
        "format": output_format,
        "provider": provider
    }

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

def measure_time(func):
    """
    함수 실행 시간 측정 데코레이터
    
    Args:
        func: 측정할 함수
    
    Returns:
        래핑된 함수
    """
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"Function {func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {str(e)}")
            raise
    
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.debug(f"Function {func.__name__} completed in {duration:.2f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {str(e)}")
            raise
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

def sanitize_prompt(prompt: str) -> str:
    """
    프롬프트 정리
    
    Args:
        prompt: 원본 프롬프트
    
    Returns:
        정리된 프롬프트
    """
    if not prompt:
        return ""
    
    # 앞뒤 공백 제거
    cleaned = prompt.strip()
    
    # 연속된 공백을 하나로 변경
    import re
    cleaned = re.sub(r'\s+', ' ', cleaned)
    
    return cleaned

def truncate_content(content: str, max_length: int = 1000) -> str:
    """
    내용 길이 제한
    
    Args:
        content: 원본 내용
        max_length: 최대 길이
    
    Returns:
        제한된 내용
    """
    if not content or len(content) <= max_length:
        return content
    
    return content[:max_length] + "..."
