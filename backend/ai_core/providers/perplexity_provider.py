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
        
        try:
            # 연결 테스트인지 확인
            is_test = len(prompt.strip()) <= 10 and prompt.strip().lower() in ['hi', 'hello', 'test']
            
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50 if is_test else 2000,
                timeout=30.0
            )
            content = response.choices[0].message.content
            return content if content is not None else ""
        except Exception as e:
            logger.error(f"Perplexity API 호출 실패: {str(e)}")
            raise
