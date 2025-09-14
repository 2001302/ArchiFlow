"""
AI 제공자 관리 클래스
"""
from typing import Optional
from ..models.enums import AIProvider
from ..providers import OpenAIProvider, AnthropicProvider, PerplexityProvider
from loguru import logger

class AIProviderManager:
    """AI 제공자 관리 클래스"""
    
    def __init__(self):
        self.providers = {
            AIProvider.PERPLEXITY: PerplexityProvider(),
            AIProvider.OPENAI: OpenAIProvider(),
            AIProvider.ANTHROPIC: AnthropicProvider()
        }
    
    async def call_provider(
        self,
        provider: AIProvider,
        prompt: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4"
    ) -> str:
        """
        AI 제공자 호출
        
        Args:
            provider: AI 제공자
            prompt: 프롬프트
            api_key: API 키 (선택사항)
            model: 모델명
        
        Returns:
            AI 응답
        """
        try:
            provider_instance = self.providers[provider]
            return await provider_instance.call_api(prompt, api_key, model)
        except Exception as e:
            logger.error(f"AI 제공자 호출 실패 ({provider.value}): {str(e)}")
            raise
