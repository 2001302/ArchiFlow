"""
유효성 검사 유틸리티
"""
from typing import Optional

def validate_api_key(api_key: Optional[str]) -> bool:
    """
    API 키 유효성 검사
    
    Args:
        api_key: API 키
    
    Returns:
        유효성 여부
    """
    return api_key is not None and len(api_key.strip()) > 0
