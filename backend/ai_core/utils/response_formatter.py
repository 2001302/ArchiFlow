"""
응답 포맷팅 유틸리티
"""
from typing import Dict, Any

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
