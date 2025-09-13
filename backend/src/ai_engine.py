"""
AI 엔진 핵심 모듈
다양한 AI API를 통합하여 사용합니다.
"""
import asyncio
from typing import Dict, Any, Optional
from loguru import logger

# PyInstaller 환경을 위한 import 처리
import sys
import os
from pathlib import Path

# PyInstaller 환경에서의 모듈 경로 처리
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행파일인 경우
    current_dir = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(os.path.dirname(sys.executable))
    src_path = current_dir / "src"
    sys.path.insert(0, str(src_path))

# 절대 import 사용 - 모든 환경에서 동일하게 동작
from ai_providers import AIProvider, AIProviderManager
from prompt_manager import PromptManager
from response_processor import ResponseProcessor
from enums import OutputFormat
from utils import (
    validate_api_key, 
    format_error_response, 
    format_success_response,
    log_api_call,
    measure_time
)

class AIEngine:
    """AI 엔진 클래스"""
    
    def __init__(self):
        self.provider_manager = AIProviderManager()
        self.prompt_manager = PromptManager()
        self.response_processor = ResponseProcessor()
    
    @measure_time
    async def generate_response(
        self,
        prompt: str,
        output_format: OutputFormat,
        provider: AIProvider = AIProvider.PERPLEXITY,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        AI 응답 생성
        
        Args:
            prompt: 사용자 프롬프트
            output_format: 출력 형식 (text, document)
            provider: AI 제공자
            language: 프로그래밍 언어
        
        Returns:
            AI 응답 딕셔너리
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            # API 키 유효성 검사
            if not validate_api_key(api_key):
                return format_error_response("API 키가 유효하지 않습니다.", provider.value)
            
            # 프롬프트 템플릿 적용
            formatted_prompt = self.prompt_manager.format_prompt(
                prompt, output_format, language
            )
            
            # AI API 호출
            response = await self.provider_manager.call_provider(
                provider, formatted_prompt, api_key, model
            )
            
            # 응답 후처리
            processed_response = self.response_processor.process_response(
                response, output_format
            )
            
            # 로깅
            duration = asyncio.get_event_loop().time() - start_time
            log_api_call(provider.value, True, duration, len(prompt))
            
            return format_success_response(
                processed_response, output_format.value, provider.value
            )
            
        except Exception as e:
            duration = asyncio.get_event_loop().time() - start_time
            log_api_call(provider.value, False, duration, len(prompt))
            logger.error(f"AI 응답 생성 실패: {str(e)}")
            return format_error_response(str(e), provider.value)
    
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
        return await self.provider_manager.test_connection(provider, api_key)