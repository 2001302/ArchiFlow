"""
기본 AI 제공자 추상 클래스
"""
from abc import ABC, abstractmethod
from typing import Optional

class BaseAIProvider(ABC):
    """AI 제공자 기본 클래스"""
    
    @abstractmethod
    async def call_api(
        self,
        prompt: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4"
    ) -> str:
        """
        AI API 호출
        
        Args:
            prompt: 프롬프트
            api_key: API 키
            model: 모델명
        
        Returns:
            AI 응답
        """
        pass
