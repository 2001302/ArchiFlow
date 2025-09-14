"""
Documize API
옵시디언 플러그인용 API 서버
ObsidianEngine을 상속받아 프로젝트 고유 기능 구현
"""

__version__ = "1.0.0"
__author__ = "Documize Team"

from .main import app, run_server

__all__ = [
    "app",
    "run_server"
]
