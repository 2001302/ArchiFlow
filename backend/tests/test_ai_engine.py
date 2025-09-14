"""
AI 엔진 유닛테스트
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
ai_core_path = Path(__file__).parent.parent / "ai_core"
sys.path.insert(0, str(ai_core_path))

from ai_core import AIEngine, AIProvider, OutputFormat
from ai_core.models.schemas import AIRequest, AIResponse, HealthResponse

class TestAIEngine:
    """AI 엔진 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.ai_engine = AIEngine()
    
    @pytest.mark.asyncio
    async def test_ai_engine_initialization(self):
        """AI 엔진 초기화 테스트"""
        assert self.ai_engine is not None
        assert self.ai_engine.provider_manager is not None
        assert self.ai_engine.prompt_manager is not None
        assert self.ai_engine.response_processor is not None
    
    @pytest.mark.asyncio
    async def test_generate_response_invalid_api_key(self):
        """유효하지 않은 API 키로 응답 생성 테스트"""
        result = await self.ai_engine.generate_response(
            prompt="Test prompt",
            output_format=OutputFormat.TEXT,
            provider=AIProvider.PERPLEXITY,
            api_key=None
        )
        
        assert result["success"] is False
        assert "API 키가 유효하지 않습니다" in result["error"]
        assert result["provider"] == "perplexity"
    
    @pytest.mark.asyncio
    async def test_generate_response_empty_api_key(self):
        """빈 API 키로 응답 생성 테스트"""
        result = await self.ai_engine.generate_response(
            prompt="Test prompt",
            output_format=OutputFormat.TEXT,
            provider=AIProvider.PERPLEXITY,
            api_key=""
        )
        
        assert result["success"] is False
        assert "API 키가 유효하지 않습니다" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_response_valid_api_key_mock(self):
        """유효한 API 키로 응답 생성 테스트 (모킹)"""
        with patch.object(self.ai_engine.provider_manager, 'call_provider', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Mocked AI response"
            
            result = await self.ai_engine.generate_response(
                prompt="Test prompt",
                output_format=OutputFormat.TEXT,
                provider=AIProvider.PERPLEXITY,
                api_key="valid_api_key"
            )
            
            assert result["success"] is True
            assert result["content"] == "Mocked AI response"
            assert result["format"] == "text"
            assert result["provider"] == "perplexity"
            mock_call.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_response_provider_error(self):
        """AI 제공자 오류 테스트"""
        with patch.object(self.ai_engine.provider_manager, 'call_provider', new_callable=AsyncMock) as mock_call:
            mock_call.side_effect = Exception("Provider error")
            
            result = await self.ai_engine.generate_response(
                prompt="Test prompt",
                output_format=OutputFormat.TEXT,
                provider=AIProvider.PERPLEXITY,
                api_key="valid_api_key"
            )
            
            assert result["success"] is False
            assert "Provider error" in result["error"]
            assert result["provider"] == "perplexity"
    
    @pytest.mark.asyncio
    async def test_generate_response_document_format(self):
        """문서 형식 응답 생성 테스트"""
        with patch.object(self.ai_engine.provider_manager, 'call_provider', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Mocked document response"
            
            result = await self.ai_engine.generate_response(
                prompt="Test document prompt",
                output_format=OutputFormat.DOCUMENT,
                provider=AIProvider.PERPLEXITY,
                api_key="valid_api_key"
            )
            
            assert result["success"] is True
            assert result["content"] == "Mocked document response"
            assert result["format"] == "document"
            assert result["provider"] == "perplexity"
    
    @pytest.mark.asyncio
    async def test_generate_response_with_language(self):
        """언어 지정 응답 생성 테스트"""
        with patch.object(self.ai_engine.provider_manager, 'call_provider', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Mocked response"
            
            result = await self.ai_engine.generate_response(
                prompt="Test prompt",
                output_format=OutputFormat.TEXT,
                provider=AIProvider.PERPLEXITY,
                api_key="valid_api_key",
                language="python"
            )
            
            assert result["success"] is True
            assert result["content"] == "Mocked response"
            mock_call.assert_called_once()
    
    def test_output_format_enum(self):
        """출력 형식 열거형 테스트"""
        assert OutputFormat.TEXT.value == "text"
        assert OutputFormat.DOCUMENT.value == "document"
    
    def test_ai_provider_enum(self):
        """AI 제공자 열거형 테스트"""
        assert AIProvider.PERPLEXITY.value == "perplexity"
        assert AIProvider.OPENAI.value == "openai"
        assert AIProvider.ANTHROPIC.value == "anthropic"
