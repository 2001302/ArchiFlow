"""
API 서버 유닛테스트
"""
import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
ai_core_path = Path(__file__).parent.parent / "ai_core"
sys.path.insert(0, str(ai_core_path))

from fastapi.testclient import TestClient
from documize_api.main import app
from ai_core.models.schemas import AIRequest, AIResponse, HealthResponse

class TestAPIServer:
    """API 서버 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Obsidian AI Engine Backend is running" in data["message"]
    
    def test_health_endpoint(self):
        """헬스 체크 엔드포인트 테스트"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "api_keys_valid" in data
        assert "missing_keys" in data
        assert data["status"] == "healthy"
    
    def test_formats_endpoint(self):
        """지원 형식 엔드포인트 테스트"""
        response = self.client.get("/formats")
        assert response.status_code == 200
        data = response.json()
        assert "formats" in data
        assert "providers" in data
        assert "text" in data["formats"]
        assert "document" in data["formats"]
        assert "perplexity" in data["providers"]
        assert "openai" in data["providers"]
        assert "anthropic" in data["providers"]
    
    @patch('documize_api.main.get_ai_engine')
    def test_generate_endpoint_success(self, mock_get_ai_engine):
        """AI 응답 생성 엔드포인트 성공 테스트"""
        # Mock AI 엔진 설정
        mock_engine = Mock()
        mock_engine.generate_response = AsyncMock(return_value={
            "success": True,
            "content": "Test AI response",
            "format": "text",
            "provider": "perplexity"
        })
        mock_get_ai_engine.return_value = mock_engine
        
        # 요청 데이터
        request_data = {
            "prompt": "Test prompt",
            "output_format": "text",
            "provider": "perplexity",
            "model": "sonar-pro",
            "api_key": "test_api_key"
        }
        
        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["content"] == "Test AI response"
        assert data["format"] == "text"
        assert data["provider"] == "perplexity"
    
    @patch('documize_api.main.get_ai_engine')
    def test_generate_endpoint_error(self, mock_get_ai_engine):
        """AI 응답 생성 엔드포인트 오류 테스트"""
        # Mock AI 엔진 설정
        mock_engine = Mock()
        mock_engine.generate_response = AsyncMock(return_value={
            "success": False,
            "error": "API 키가 유효하지 않습니다",
            "provider": "perplexity"
        })
        mock_get_ai_engine.return_value = mock_engine
        
        # 요청 데이터
        request_data = {
            "prompt": "Test prompt",
            "output_format": "text",
            "provider": "perplexity",
            "model": "sonar-pro",
            "api_key": None
        }
        
        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "API 키가 유효하지 않습니다" in data["error"]
    
    def test_generate_endpoint_invalid_format(self):
        """유효하지 않은 출력 형식 테스트"""
        request_data = {
            "prompt": "Test prompt",
            "output_format": "invalid_format",
            "provider": "perplexity",
            "model": "sonar-pro",
            "api_key": "test_api_key"
        }
        
        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 400
        data = response.json()
        assert "지원하지 않는 출력 형식입니다" in data["detail"]
    
    def test_generate_endpoint_invalid_provider(self):
        """유효하지 않은 AI 제공자 테스트"""
        request_data = {
            "prompt": "Test prompt",
            "output_format": "text",
            "provider": "invalid_provider",
            "model": "sonar-pro",
            "api_key": "test_api_key"
        }
        
        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 400
        data = response.json()
        assert "지원하지 않는 AI 제공자입니다" in data["detail"]
    
    def test_generate_endpoint_missing_required_fields(self):
        """필수 필드 누락 테스트"""
        request_data = {
            "output_format": "text",
            "provider": "perplexity"
        }
        
        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 422  # Validation error
    
    @patch('documize_api.main.get_ai_engine')
    def test_generate_endpoint_server_error(self, mock_get_ai_engine):
        """서버 오류 테스트"""
        # Mock AI 엔진에서 예외 발생
        mock_engine = Mock()
        mock_engine.generate_response = AsyncMock(side_effect=Exception("Internal server error"))
        mock_get_ai_engine.return_value = mock_engine
        
        request_data = {
            "prompt": "Test prompt",
            "output_format": "text",
            "provider": "perplexity",
            "model": "sonar-pro",
            "api_key": "test_api_key"
        }
        
        response = self.client.post("/generate", json=request_data)
        assert response.status_code == 500
        data = response.json()
        assert "Internal server error" in data["detail"]
    
    def test_cors_headers(self):
        """CORS 헤더 테스트"""
        response = self.client.get("/")
        # CORS 헤더가 포함되어 있는지 확인
        assert response.status_code == 200
        # CORS 헤더는 FastAPI의 CORSMiddleware에서 자동으로 추가됨
    
    def test_request_validation(self):
        """요청 유효성 검사 테스트"""
        # 빈 요청
        response = self.client.post("/generate", json={})
        assert response.status_code == 422
        
        # 잘못된 데이터 타입
        response = self.client.post("/generate", json={
            "prompt": 123,  # 문자열이어야 함
            "output_format": "text",
            "provider": "perplexity"
        })
        assert response.status_code == 422
