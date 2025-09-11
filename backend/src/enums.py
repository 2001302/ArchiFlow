"""
공통 열거형 정의 모듈
"""
from enum import Enum

class OutputFormat(Enum):
    """출력 형식 열거형"""
    MERMAID = "mermaid"
    SOURCE_CODE = "source_code"
    TEXT = "text"
