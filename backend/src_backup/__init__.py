"""
Arch Flow Backend Package
모든 모듈의 import를 중앙화하여 관리합니다.
"""
import sys

# PyInstaller 환경 감지 (한 곳에서만)
IS_FROZEN = getattr(sys, 'frozen', False)

# 공통 import 로직
if IS_FROZEN:
    # PyInstaller로 빌드된 실행파일인 경우 - 절대 import
    from config import settings
    from enums import OutputFormat
    from utils import (
        validate_api_key, 
        format_error_response, 
        format_success_response,
        log_api_call,
        measure_time,
        sanitize_prompt,
        truncate_content
    )
else:
    # 개발 환경인 경우 - 상대 import
    from .config import settings
    from .enums import OutputFormat
    from .utils import (
        validate_api_key, 
        format_error_response, 
        format_success_response,
        log_api_call,
        measure_time,
        sanitize_prompt,
        truncate_content
    )

# 모든 클래스를 패키지 레벨에서 import (지연 import로 순환 참조 방지)
def _lazy_import():
    """지연 import를 위한 함수"""
    from .ai_engine import AIEngine
    from .ai_providers import AIProvider, AIProviderManager
    from .prompt_manager import PromptManager
    from .response_processor import ResponseProcessor
    
    return {
        'AIEngine': AIEngine,
        'AIProvider': AIProvider,
        'AIProviderManager': AIProviderManager,
        'PromptManager': PromptManager,
        'ResponseProcessor': ResponseProcessor
    }

# 지연 import를 위한 모듈 레벨 변수
_imported_classes = None

def __getattr__(name):
    """지연 import를 위한 매직 메서드"""
    global _imported_classes
    if _imported_classes is None:
        _imported_classes = _lazy_import()
    return _imported_classes[name]

# 패키지에서 노출할 모든 항목들 (지연 import된 클래스들은 제외)
__all__ = [
    # 열거형
    'OutputFormat',
    
    # 설정
    'settings',
    
    # 유틸리티 함수들
    'validate_api_key', 
    'format_error_response',
    'format_success_response',
    'log_api_call',
    'measure_time',
    'sanitize_prompt',
    'truncate_content',
    
    # 환경 변수
    'IS_FROZEN'
]
