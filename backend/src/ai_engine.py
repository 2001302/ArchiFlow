"""
AI 엔진 핵심 모듈
다양한 AI API를 통합하여 사용합니다.
"""
import asyncio
from typing import Dict, Any, Optional, List
from enum import Enum
import httpx
from loguru import logger

from .config import settings

class OutputFormat(Enum):
    """출력 형식 열거형"""
    MERMAID = "mermaid"
    SOURCE_CODE = "source_code"
    TEXT = "text"

class AIProvider(Enum):
    """AI 제공자 열거형"""
    PERPLEXITY = "perplexity"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class AIEngine:
    """AI 엔진 클래스"""
    
    def __init__(self):
        self.providers = {
            AIProvider.PERPLEXITY: self._call_perplexity,
            AIProvider.OPENAI: self._call_openai,
            AIProvider.ANTHROPIC: self._call_anthropic
        }
    
    async def generate_response(
        self,
        prompt: str,
        output_format: OutputFormat,
        provider: AIProvider = AIProvider.PERPLEXITY,
        api_key: Optional[str] = None,
        source_code: Optional[str] = None,
        diagram_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        AI 응답 생성
        
        Args:
            prompt: 사용자 프롬프트
            output_format: 출력 형식 (mermaid, source_code, text)
            provider: AI 제공자
            source_code: 소스코드 컨텍스트
            diagram_context: 다이어그램 컨텍스트
        
        Returns:
            AI 응답 딕셔너리
        """
        try:
            # 프롬프트 템플릿 적용
            formatted_prompt = self._format_prompt(
                prompt, output_format, source_code, diagram_context
            )
            
            # AI API 호출
            response = await self.providers[provider](formatted_prompt, api_key)
            
            # 응답 후처리
            processed_response = self._post_process_response(
                response, output_format
            )
            
            return {
                "success": True,
                "content": processed_response,
                "format": output_format.value,
                "provider": provider.value
            }
            
        except Exception as e:
            logger.error(f"AI 응답 생성 실패: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def _format_prompt(
        self,
        prompt: str,
        output_format: OutputFormat,
        source_code: Optional[str] = None,
        diagram_context: Optional[str] = None
    ) -> str:
        """프롬프트 포맷팅"""
        
        # 기본 프롬프트 템플릿
        templates = {
            OutputFormat.MERMAID: """
다음 요청에 대해 Mermaid 다이어그램 문법으로 답변해주세요.
요청: {prompt}

다이어그램 컨텍스트: {diagram_context}

소스코드 컨텍스트: {source_code}

답변은 반드시 ```mermaid로 시작하고 ```로 끝나는 코드 블록 형태로 제공해주세요.
""",
            OutputFormat.SOURCE_CODE: """
다음 요청에 대해 소스코드로 답변해주세요.
요청: {prompt}

다이어그램 컨텍스트: {diagram_context}

소스코드 컨텍스트: {source_code}

답변은 반드시 ```{language}로 시작하고 ```로 끝나는 코드 블록 형태로 제공해주세요.
""",
            OutputFormat.TEXT: """
다음 요청에 대해 텍스트로 답변해주세요.
요청: {prompt}

다이어그램 컨텍스트: {diagram_context}

소스코드 컨텍스트: {source_code}
"""
        }
        
        template = templates[output_format]
        return template.format(
            prompt=prompt,
            diagram_context=diagram_context or "없음",
            source_code=source_code or "없음",
            language="python"  # 기본 언어
        )
    
    def _post_process_response(
        self, 
        response: str, 
        output_format: OutputFormat
    ) -> str:
        """응답 후처리"""
        if output_format == OutputFormat.MERMAID:
            # Mermaid 코드 블록 추출
            if "```mermaid" in response:
                start = response.find("```mermaid") + 10
                end = response.find("```", start)
                if end != -1:
                    return response[start:end].strip()
            return response
        
        elif output_format == OutputFormat.SOURCE_CODE:
            # 소스코드 블록 추출
            if "```" in response:
                start = response.find("```") + 3
                end = response.find("```", start)
                if end != -1:
                    return response[start:end].strip()
            return response
        
        return response
    
    async def _call_perplexity(self, prompt: str, api_key: Optional[str] = None) -> str:
        """Perplexity API 호출"""
        # 클라이언트에서 전달받은 API Key 우선 사용, 없으면 설정에서 가져오기
        key = api_key or settings.perplexity_api_key
        if not key:
            raise ValueError("Perplexity API 키가 설정되지 않았습니다.")
        
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def _call_openai(self, prompt: str, api_key: Optional[str] = None) -> str:
        """OpenAI API 호출"""
        # 클라이언트에서 전달받은 API Key 우선 사용, 없으면 설정에서 가져오기
        key = api_key or settings.openai_api_key
        if not key:
            raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
        
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def _call_anthropic(self, prompt: str, api_key: Optional[str] = None) -> str:
        """Anthropic API 호출"""
        # 클라이언트에서 전달받은 API Key 우선 사용, 없으면 설정에서 가져오기
        key = api_key or settings.anthropic_api_key
        if not key:
            raise ValueError("Anthropic API 키가 설정되지 않았습니다.")
        
        headers = {
            "x-api-key": key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"]
