"""
AI 제공자 유닛테스트
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
ai_core_path = Path(__file__).parent.parent / "ai_core"
sys.path.insert(0, str(ai_core_path))

from ai_core.providers import PerplexityProvider, OpenAIProvider, AnthropicProvider
from ai_core.models.enums import AIProvider

class TestPerplexityProvider:
    """Perplexity 제공자 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.provider = PerplexityProvider()
    
    @pytest.mark.asyncio
    async def test_call_api_missing_api_key(self):
        """API 키 누락 테스트"""
        with pytest.raises(ValueError, match="Perplexity API 키가 설정되지 않았습니다"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key=None,
                model="sonar-pro"
            )
    
    @pytest.mark.asyncio
    async def test_call_api_empty_api_key(self):
        """빈 API 키 테스트"""
        with pytest.raises(ValueError, match="Perplexity API 키가 설정되지 않았습니다"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key="",
                model="sonar-pro"
            )
    
    @pytest.mark.asyncio
    @patch('ai_core.providers.perplexity_provider.AsyncOpenAI')
    async def test_call_api_success(self, mock_openai):
        """API 호출 성공 테스트"""
        # Mock OpenAI 클라이언트 설정
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
        
        result = await self.provider.call_api(
            prompt="Test prompt",
            api_key="test_api_key",
            model="sonar-pro"
        )
        
        assert result == "Test response"
        mock_client.chat.completions.create.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('ai_core.providers.perplexity_provider.AsyncOpenAI')
    async def test_call_api_error(self, mock_openai):
        """API 호출 오류 테스트"""
        # Mock OpenAI 클라이언트에서 예외 발생
        mock_client = Mock()
        mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API error"))
        mock_openai.return_value = mock_client
        
        with pytest.raises(Exception, match="API error"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key="test_api_key",
                model="sonar-pro"
            )

class TestOpenAIProvider:
    """OpenAI 제공자 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.provider = OpenAIProvider()
    
    @pytest.mark.asyncio
    async def test_call_api_missing_api_key(self):
        """API 키 누락 테스트"""
        with pytest.raises(ValueError, match="OpenAI API 키가 설정되지 않았습니다"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key=None,
                model="gpt-4"
            )
    
    @pytest.mark.asyncio
    @patch('ai_core.providers.openai_provider.httpx.AsyncClient')
    async def test_call_api_success(self, mock_httpx):
        """API 호출 성공 테스트"""
        # Mock HTTP 클라이언트 설정
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        mock_response.raise_for_status.return_value = None
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_httpx.return_value = mock_client
        
        result = await self.provider.call_api(
            prompt="Test prompt",
            api_key="test_api_key",
            model="gpt-4"
        )
        
        assert result == "Test response"
        mock_client.post.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('ai_core.providers.openai_provider.httpx.AsyncClient')
    async def test_call_api_error(self, mock_httpx):
        """API 호출 오류 테스트"""
        # Mock HTTP 클라이언트에서 예외 발생
        mock_client = Mock()
        mock_client.post = AsyncMock(side_effect=Exception("HTTP error"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_httpx.return_value = mock_client
        
        with pytest.raises(Exception, match="HTTP error"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key="test_api_key",
                model="gpt-4"
            )

class TestAnthropicProvider:
    """Anthropic 제공자 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.provider = AnthropicProvider()
    
    @pytest.mark.asyncio
    async def test_call_api_missing_api_key(self):
        """API 키 누락 테스트"""
        with pytest.raises(ValueError, match="Anthropic API 키가 설정되지 않았습니다"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key=None,
                model="claude-3"
            )
    
    @pytest.mark.asyncio
    @patch('ai_core.providers.anthropic_provider.httpx.AsyncClient')
    async def test_call_api_success(self, mock_httpx):
        """API 호출 성공 테스트"""
        # Mock HTTP 클라이언트 설정
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "content": [{"text": "Test response"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_httpx.return_value = mock_client
        
        result = await self.provider.call_api(
            prompt="Test prompt",
            api_key="test_api_key",
            model="claude-3"
        )
        
        assert result == "Test response"
        mock_client.post.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('ai_core.providers.anthropic_provider.httpx.AsyncClient')
    async def test_call_api_error(self, mock_httpx):
        """API 호출 오류 테스트"""
        # Mock HTTP 클라이언트에서 예외 발생
        mock_client = Mock()
        mock_client.post = AsyncMock(side_effect=Exception("HTTP error"))
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_httpx.return_value = mock_client
        
        with pytest.raises(Exception, match="HTTP error"):
            await self.provider.call_api(
                prompt="Test prompt",
                api_key="test_api_key",
                model="claude-3"
            )

class TestProviderManager:
    """AI 제공자 관리자 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        from ai_core.managers.provider_manager import AIProviderManager
        self.manager = AIProviderManager()
    
    def test_provider_initialization(self):
        """제공자 초기화 테스트"""
        assert AIProvider.PERPLEXITY in self.manager.providers
        assert AIProvider.OPENAI in self.manager.providers
        assert AIProvider.ANTHROPIC in self.manager.providers
    
    @pytest.mark.asyncio
    async def test_call_provider_success(self):
        """제공자 호출 성공 테스트"""
        with patch.object(self.manager.providers[AIProvider.PERPLEXITY], 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = "Test response"
            
            result = await self.manager.call_provider(
                provider=AIProvider.PERPLEXITY,
                prompt="Test prompt",
                api_key="test_api_key",
                model="sonar-pro"
            )
            
            assert result == "Test response"
            mock_call.assert_called_once_with("Test prompt", "test_api_key", "sonar-pro")
    
    @pytest.mark.asyncio
    async def test_call_provider_error(self):
        """제공자 호출 오류 테스트"""
        with patch.object(self.manager.providers[AIProvider.PERPLEXITY], 'call_api', new_callable=AsyncMock) as mock_call:
            mock_call.side_effect = Exception("Provider error")
            
            with pytest.raises(Exception, match="Provider error"):
                await self.manager.call_provider(
                    provider=AIProvider.PERPLEXITY,
                    prompt="Test prompt",
                    api_key="test_api_key",
                    model="sonar-pro"
                )
