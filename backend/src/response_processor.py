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
    
    # 절대 import 사용
    from enums import OutputFormat
else:
    # 개발 환경인 경우 - 상대 import 사용
    from .enums import OutputFormat

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
        if output_format == OutputFormat.MERMAID:
            return self._process_mermaid_response(response)
        elif output_format == OutputFormat.SOURCE_CODE:
            return self._process_source_code_response(response)
        else:
            return response
    
    def _process_mermaid_response(self, response: str) -> str:
        """Mermaid 응답 처리"""
        # Mermaid 코드 블록 추출
        if "```mermaid" in response:
            start = response.find("```mermaid") + 10
            end = response.find("```", start)
            if end != -1:
                mermaid_code = response[start:end].strip()
                cleaned_code = self._clean_mermaid_code(mermaid_code)
                return f"```mermaid\n{cleaned_code}\n```"
        
        # Mermaid 코드 블록이 없으면 전체 응답을 mermaid 블록으로 감싸기
        return f"```mermaid\n{self._clean_mermaid_code(response)}\n```"
    
    def _process_source_code_response(self, response: str) -> str:
        """소스코드 응답 처리"""
        # 소스코드 블록 추출
        if "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            if end != -1:
                code = response[start:end].strip()
                cleaned_code = self._clean_source_code(code)
                language = self._detect_code_language(cleaned_code) or "python"
                return f"```{language}\n{cleaned_code}\n```"
        
        # 코드 블록이 없으면 전체 응답을 코드 블록으로 감싸기
        return f"```python\n{self._clean_source_code(response)}\n```"
    
    def _clean_mermaid_code(self, code: str) -> str:
        """Mermaid 코드 정리"""
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):  # 주석 제거
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _clean_source_code(self, code: str) -> str:
        """소스코드 정리"""
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 불필요한 공백 제거하되 들여쓰기는 유지
            if line.strip():  # 빈 줄이 아닌 경우만
                cleaned_lines.append(line)
            elif cleaned_lines and cleaned_lines[-1].strip():  # 이전 줄이 비어있지 않으면
                cleaned_lines.append('')  # 빈 줄 유지
        
        return '\n'.join(cleaned_lines)
    
    def _detect_code_language(self, code: str) -> Optional[str]:
        """코드에서 프로그래밍 언어 감지"""
        code_lower = code.lower().strip()
        
        # Python 키워드
        if any(keyword in code_lower for keyword in ['def ', 'import ', 'from ', 'class ', 'if __name__']):
            return 'python'
        
        # JavaScript/TypeScript 키워드
        if any(keyword in code_lower for keyword in ['function', 'const ', 'let ', 'var ', '=>', 'interface ']):
            if 'interface ' in code_lower or ': ' in code_lower:
                return 'typescript'
            return 'javascript'
        
        # Java 키워드
        if any(keyword in code_lower for keyword in ['public class', 'private ', 'public ', 'System.out.println']):
            return 'java'
        
        # C/C++ 키워드
        if any(keyword in code_lower for keyword in ['#include', 'int main', 'std::', 'cout <<']):
            if 'std::' in code_lower or 'cout <<' in code_lower:
                return 'cpp'
            return 'c'
        
        # HTML 키워드
        if any(keyword in code_lower for keyword in ['<html>', '<div>', '<span>', '<!DOCTYPE']):
            return 'html'
        
        # CSS 키워드
        if any(keyword in code_lower for keyword in ['{', '}', 'margin:', 'padding:', 'color:']):
            return 'css'
        
        # SQL 키워드
        if any(keyword in code_lower for keyword in ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE']):
            return 'sql'
        
        # Go 키워드
        if any(keyword in code_lower for keyword in ['package ', 'func ', 'import ', 'var ', 'const ']):
            return 'go'
        
        # Rust 키워드
        if any(keyword in code_lower for keyword in ['fn ', 'let ', 'mut ', 'use ', 'struct ', 'impl ']):
            return 'rust'
        
        # 기본값
        return None
