"""
공통 열거형 정의 모듈
"""
from enum import Enum

class OutputFormat(Enum):
    """출력 형식 열거형"""
    TEXT = "text"
    DOCUMENT = "document"

class AIProvider(Enum):
    """AI 제공자 열거형"""
    PERPLEXITY = "perplexity"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
