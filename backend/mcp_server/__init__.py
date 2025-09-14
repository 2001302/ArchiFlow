"""
AI Core Library
범용 AI 기능을 제공하는 핵심 라이브러리
"""

__version__ = "1.0.0"
__author__ = "Documize Team"

from .managers.mcp_engine import MCPEngine
from .managers.provider_manager import AIProviderManager
from .models.enums import AIProvider, OutputFormat
from .config.settings import AICoreSettings

__all__ = [
    "MCPEngine",
    "AIProviderManager", 
    "AIProvider",
    "OutputFormat",
    "AICoreSettings"
]
