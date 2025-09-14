"""
AI Core 설정 관리
"""
import os
import sys
import json
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 로드
load_dotenv()

def get_log_file_path() -> str:
    """로그 파일 경로를 동적으로 결정합니다."""
    try:
        # PyInstaller 환경에서의 경로 처리
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 실행파일인 경우
            # 실행파일과 같은 디렉토리의 logs 폴더 사용
            current_dir = Path(os.path.dirname(sys.executable))
            log_dir = current_dir / "logs"
            log_dir.mkdir(exist_ok=True)
            return str(log_dir / "ai_engine.log")
        else:
            # 개발 환경인 경우 - 루트의 logs 폴더 사용
            project_root = Path(__file__).parent.parent.parent.parent
            log_dir = project_root / "logs"
            log_dir.mkdir(exist_ok=True)
            return str(log_dir / "ai_engine.log")
    except Exception as e:
        print(f"로그 파일 경로 설정 실패: {e}")
        return "logs/ai_engine.log"

class AICoreSettings(BaseSettings):
    """AI Core 설정"""
    
    # AI API Keys
    perplexity_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # AI Request Mode
    ai_request_mode: str = "mcp"  # "direct" or "mcp"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = get_log_file_path()
    
    class Config:
        env_file = ".env"
        case_sensitive = False

def load_config_json() -> Dict[str, Any]:
    """config.json 파일을 로드합니다."""
    try:
        # PyInstaller 환경에서의 경로 처리
        if getattr(sys, 'frozen', False):
            # PyInstaller로 빌드된 실행파일인 경우
            current_dir = Path(getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)))
            config_path = current_dir / "config.json"
        else:
            # 개발 환경인 경우
            config_path = Path(__file__).parent.parent.parent.parent / "config.json"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        print(f"config.json 로드 실패: {e}")
        return {}

# config.json에서 설정 로드
config_data = load_config_json()
provider_configs = config_data.get('providers', {})
ai_request_mode = config_data.get('ai_request_mode', 'mcp')

# API 키 검증
def validate_api_keys() -> dict:
    """API 키 유효성 검사"""
    missing_keys = []
    
    if not settings.perplexity_api_key:
        missing_keys.append("PERPLEXITY_API_KEY")
    if not settings.openai_api_key:
        missing_keys.append("OPENAI_API_KEY")
    if not settings.anthropic_api_key:
        missing_keys.append("ANTHROPIC_API_KEY")
    
    return {
        "valid": len(missing_keys) == 0,
        "missing_keys": missing_keys
    }

# 전역 설정 인스턴스
settings = AICoreSettings()

# config.json에서 AI 모드 설정 적용
if ai_request_mode:
    settings.ai_request_mode = ai_request_mode
