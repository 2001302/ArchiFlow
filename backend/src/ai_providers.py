"""
AI 제공자 관리 모듈
다양한 AI API 제공자를 통합하여 관리합니다.
"""
import httpx
from typing import Optional, Dict, Any
from enum import Enum
from openai import AsyncOpenAI
from loguru import logger

# PyInstaller 환경을 위한 import 처리
import sys
import os
from pathlib import Path

# PyInstaller 환경에서의 모듈 경로 처리
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행파일인 경우
    current_dir = Path(getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)))
    src_path = current_dir / "src"
    sys.path.insert(0, str(src_path))

# 절대 import 사용 - 모든 환경에서 동일하게 동작
from config import settings, provider_configs

class AIProvider(Enum):
    """AI 제공자 열거형"""
    PERPLEXITY = "perplexity"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class AIProviderManager:
    """AI 제공자 관리 클래스"""
    
    def __init__(self):
        self.providers = {
            AIProvider.PERPLEXITY: self._call_perplexity,
            AIProvider.OPENAI: self._call_openai,
            AIProvider.ANTHROPIC: self._call_anthropic
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
        
        Returns:
            AI 응답
        """
        try:
            return await self.providers[provider](prompt, api_key, model)
        except Exception as e:
            logger.error(f"AI 제공자 호출 실패 ({provider.value}): {str(e)}")
            raise
    
    async def _call_perplexity(self, prompt: str, api_key: Optional[str] = None, model: str = "gpt-4") -> str:
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
    
    async def _call_openai(self, prompt: str, api_key: Optional[str] = None, model: str = "gpt-4") -> str:
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
    
    async def _call_anthropic(self, prompt: str, api_key: Optional[str] = None, model: str = "gpt-4") -> str:
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
    
    async def test_connection(
        self,
        provider: AIProvider,
        api_key: str
    ) -> Dict[str, Any]:
        """
        API 연결 테스트
        
        Args:
            provider: AI 제공자
            api_key: API 키
        
        Returns:
            테스트 결과 딕셔너리
        """
        try:
            test_prompt = "Hi"
            response = await self.providers[provider](test_prompt, api_key)
            
            if response and len(response.strip()) > 0:
                return {
                    "success": True,
                    "message": f"{provider.value} API 연결이 성공적으로 확인되었습니다."
                }
            else:
                return {
                    "success": False,
                    "message": f"{provider.value} API에서 빈 응답을 받았습니다."
                }
            
        except Exception as e:
            logger.error(f"API 연결 테스트 실패 ({provider.value}): {str(e)}")
            return {
                "success": False,
                "message": f"{provider.value} API 연결에 실패했습니다: {str(e)}"
            }
