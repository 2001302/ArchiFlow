"""
Perplexity 제공자
"""
from typing import Optional
from openai import AsyncOpenAI
from .base_provider import BaseAIProvider
from ..config.settings import settings, provider_configs
from loguru import logger

class PerplexityProvider(BaseAIProvider):
    """Perplexity API 제공자"""
    
    async def call_api(
        self,
        prompt: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4"
    ) -> str:
        """Perplexity API 호출"""
        key = api_key or settings.perplexity_api_key
        if not key:
            raise ValueError("Perplexity API 키가 설정되지 않았습니다.")
        
        # config.json에서 API URL 가져오기
        perplexity_config = provider_configs.get('perplexity', {})
        base_url = perplexity_config.get('api_url', 'https://api.perplexity.ai')
        
        client = AsyncOpenAI(
            api_key=key,
            base_url=base_url
        )
        