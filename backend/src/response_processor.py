"""
응답 후처리 모듈
AI 응답을 적절한 형식으로 정리하고 포맷팅합니다.
"""
from typing import Optional

# PyInstaller 환경을 위한 import 처리
import sys
import os
from pathlib import Path

# PyInstaller 환경에서의 모듈 경로 처리
if getattr(sys, 'frozen', False):
    # PyInstaller로 빌드된 실행파일인 경우
    current_dir = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(os.path.dirname(sys.executable))
    src_path = current_dir / "src"
    sys.path.insert(0, str(src_path))

# 절대 import 사용 - 모든 환경에서 동일하게 동작
from enums import OutputFormat

class ResponseProcessor:
    """응답 후처리 클래스"""
    
    def process_response(
        self, 
        response: str, 
        output_format: OutputFormat
    ) -> str:
        """
        응답 후처리
        
        Args:
            response: AI 응답
            output_format: 출력 형식
        
        Returns:
            처리된 응답
        """
        return response
    
    
