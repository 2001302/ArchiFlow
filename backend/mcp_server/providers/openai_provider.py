"""
OpenAI 제공자
"""
import httpx
from typing import Optional
from .base_provider import BaseAIProvider
from ..config.settings import settings, provider_configs
from loguru import logger

class OpenAIProvider(BaseAIProvider):
    """OpenAI API 제공자"""
    
    async def call_api(
        self,
        prompt: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4"
    ) -> str:
        """OpenAI API 호출"""
        key = api_key or settings.openai_api_key
        if not key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
        
        # config.json에서 API URL과 인증 방식 가져오기
        openai_config = provider_configs.get('openai', {})
        api_url = openai_config.get('api_url', 'https://api.openai.com/v1/chat/completions')
        auth_header = openai_config.get('auth_header', 'Authorization')
        auth_prefix = openai_config.get('auth_prefix', 'Bearer')
        
        headers = {
            auth_header: f"{auth_prefix} {key}".strip(),
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
