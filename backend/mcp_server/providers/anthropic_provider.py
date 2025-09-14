"""
Anthropic 제공자
"""
import httpx
from typing import Optional
from .base_provider import BaseAIProvider
from ..config.settings import settings, provider_configs
from loguru import logger

class AnthropicProvider(BaseAIProvider):
    """Anthropic API 제공자"""
    
    async def call_api(
        self,
        prompt: str,
        api_key: Optional[str] = None,
        model: str = "gpt-4"
    ) -> str:
        """Anthropic API 호출"""
        key = api_key or settings.anthropic_api_key
        if not key:
            raise ValueError("Anthropic API 키가 설정되지 않았습니다.")
        
        # config.json에서 API URL과 인증 방식 가져오기
        anthropic_config = provider_configs.get('anthropic', {})
        api_url = anthropic_config.get('api_url', 'https://api.anthropic.com/v1/messages')
        auth_header = anthropic_config.get('auth_header', 'x-api-key')
        auth_prefix = anthropic_config.get('auth_prefix', '')
        
        headers = {
            auth_header: f"{auth_prefix}{key}".strip(),
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": model,
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
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
            return result["content"][0]["text"] or ""
