"""
pytest 설정 및 픽스처
"""
import pytest
import asyncio
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
ai_core_path = Path(__file__).parent.parent / "ai_core"
sys.path.insert(0, str(ai_core_path))

@pytest.fixture(scope="session")
def event_loop():
    """비동기 테스트를 위한 이벤트 루프 픽스처"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_api_key():
    """테스트용 API 키 픽스처"""
    return "test_api_key_12345"

@pytest.fixture
def mock_prompt():
    """테스트용 프롬프트 픽스처"""
    return "Test prompt for unit testing"

@pytest.fixture
def mock_ai_response():
    """테스트용 AI 응답 픽스처"""
    return "This is a test AI response"

@pytest.fixture
def mock_error_response():
    """테스트용 에러 응답 픽스처"""
    return "Test error message"

@pytest.fixture
def sample_config():
    """테스트용 설정 픽스처"""
    return {
        "providers": {
            "perplexity": {
                "api_url": "https://api.perplexity.ai",
                "auth_header": "Authorization",
                "auth_prefix": "Bearer"
            },
            "openai": {
                "api_url": "https://api.openai.com/v1/chat/completions",
                "auth_header": "Authorization",
                "auth_prefix": "Bearer"
            },
            "anthropic": {
                "api_url": "https://api.anthropic.com/v1/messages",
                "auth_header": "x-api-key",
                "auth_prefix": ""
            }
        }
    }
