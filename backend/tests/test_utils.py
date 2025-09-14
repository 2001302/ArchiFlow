"""
유틸리티 유닛테스트
"""
import pytest
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
mcp_server_path = Path(__file__).parent.parent / "mcp_server"
sys.path.insert(0, str(mcp_server_path))

from mcp_server.utils.validation import validate_api_key
from mcp_server.utils.response_formatter import format_error_response, format_success_response
from mcp_server.utils.logging import log_api_call
from mcp_server.utils.decorators import measure_time

class TestValidation:
    """유효성 검사 테스트 클래스"""
    
    def test_validate_api_key_valid(self):
        """유효한 API 키 테스트"""
        assert validate_api_key("valid_api_key") is True
        assert validate_api_key("  valid_api_key  ") is True
        assert validate_api_key("sk-1234567890abcdef") is True
    
    def test_validate_api_key_invalid(self):
        """유효하지 않은 API 키 테스트"""
        assert validate_api_key(None) is False
        assert validate_api_key("") is False
        assert validate_api_key("   ") is False
        assert validate_api_key("\t\n") is False

class TestResponseFormatter:
    """응답 포맷터 테스트 클래스"""
    
    def test_format_error_response(self):
        """에러 응답 포맷팅 테스트"""
        result = format_error_response("Test error", "perplexity")
        
        assert result["success"] is False
        assert result["error"] == "Test error"
        assert result["content"] is None
        assert result["provider"] == "perplexity"
    
    def test_format_error_response_default_provider(self):
        """기본 제공자로 에러 응답 포맷팅 테스트"""
        result = format_error_response("Test error")
        
        assert result["success"] is False
        assert result["error"] == "Test error"
        assert result["content"] is None
        assert result["provider"] == "unknown"
    
    def test_format_success_response(self):
        """성공 응답 포맷팅 테스트"""
        result = format_success_response("Test content", "text", "perplexity")
        
        assert result["success"] is True
        assert result["content"] == "Test content"
        assert result["format"] == "text"
        assert result["provider"] == "perplexity"
    
    def test_format_success_response_document(self):
        """문서 형식 성공 응답 포맷팅 테스트"""
        result = format_success_response("Document content", "document", "openai")
        
        assert result["success"] is True
        assert result["content"] == "Document content"
        assert result["format"] == "document"
        assert result["provider"] == "openai"

class TestLogging:
    """로깅 테스트 클래스"""
    
    def test_log_api_call_success(self):
        """성공 API 호출 로깅 테스트"""
        # 로깅 함수가 예외 없이 실행되는지 확인
        log_api_call("perplexity", True, 1.5, 100)
        log_api_call("openai", True, 2.0, 200)
        log_api_call("anthropic", True, 0.5, 50)
    
    def test_log_api_call_failure(self):
        """실패 API 호출 로깅 테스트"""
        # 로깅 함수가 예외 없이 실행되는지 확인
        log_api_call("perplexity", False, 1.5, 100)
        log_api_call("openai", False, 2.0, 200)
        log_api_call("anthropic", False, 0.5, 50)
    
    def test_log_api_call_zero_duration(self):
        """0초 소요 시간 로깅 테스트"""
        log_api_call("perplexity", True, 0.0, 100)
    
    def test_log_api_call_zero_prompt_length(self):
        """0 길이 프롬프트 로깅 테스트"""
        log_api_call("perplexity", True, 1.0, 0)

class TestDecorators:
    """데코레이터 테스트 클래스"""
    
    def test_measure_time_sync_function(self):
        """동기 함수 시간 측정 테스트"""
        @measure_time
        def test_function(x, y):
            return x + y
        
        result = test_function(1, 2)
        assert result == 3
    
    @pytest.mark.asyncio
    async def test_measure_time_async_function(self):
        """비동기 함수 시간 측정 테스트"""
        @measure_time
        async def test_async_function(x, y):
            return x + y
        
        result = await test_async_function(1, 2)
        assert result == 3
    
    def test_measure_time_sync_function_error(self):
        """동기 함수 오류 시간 측정 테스트"""
        @measure_time
        def test_error_function():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            test_error_function()
    
    @pytest.mark.asyncio
    async def test_measure_time_async_function_error(self):
        """비동기 함수 오류 시간 측정 테스트"""
        @measure_time
        async def test_async_error_function():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError, match="Test error"):
            await test_async_error_function()
