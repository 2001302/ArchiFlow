"""
프롬프트 매니저 모듈
다양한 출력 형식에 맞는 프롬프트 템플릿을 관리합니다.
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

class PromptManager:
    """프롬프트 매니저 클래스"""
    
    def format_prompt(
        self,
        prompt: str,
        output_format: OutputFormat,
        source_code: Optional[str] = None,
        diagram_context: Optional[str] = None,
        language: Optional[str] = None
    ) -> str:
        """
        프롬프트 포맷팅
        
        Args:
            prompt: 사용자 프롬프트
            output_format: 출력 형식
            source_code: 소스코드 컨텍스트
            diagram_context: 다이어그램 컨텍스트
            language: 프로그래밍 언어
        
        Returns:
            포맷된 프롬프트
        """
        templates = {
            OutputFormat.MERMAID: self._get_mermaid_template(),
            OutputFormat.SOURCE_CODE: self._get_source_code_template(),
            OutputFormat.TEXT: self._get_text_template()
        }
        
        template = templates[output_format]
        return template.format(
            prompt=prompt,
            diagram_context=diagram_context or "None",
            source_code=source_code or "None",
            language=language or "python"
        )
    
    def _get_mermaid_template(self) -> str:
        """Mermaid 다이어그램 템플릿"""
        return """
Please generate a Mermaid diagram based on the following request.

Request: {prompt}

Existing diagram context:
{diagram_context}

Related source code:
{source_code}

Instructions:
1. Use correct Mermaid syntax
2. Make the diagram clear and easy to understand
3. Clearly express relationships and flows
4. Provide your answer in a code block that starts with ```mermaid and ends with ```

Answer:
"""
    
    def _get_source_code_template(self) -> str:
        """소스코드 템플릿"""
        return """
Please provide a {language} source code solution for the following request.

Request: {prompt}

Existing diagram context:
{diagram_context}

Related source code:
{source_code}

Instructions:
1. Use correct {language} syntax
2. The code should be executable and efficient
3. Include appropriate comments
4. Provide your answer in a code block that starts with ```{language} and ends with ```

Answer:
"""
    
    def _get_text_template(self) -> str:
        """일반 텍스트 템플릿"""
        return """
Please help with the following request.

Request: {prompt}

Existing diagram context:
{diagram_context}

Related source code:
{source_code}

Instructions:
1. Provide accurate and useful information
2. Include examples or explanations when necessary
3. Respond in Korean

Answer:
"""
    
    def get_supported_languages(self) -> list:
        """지원하는 프로그래밍 언어 목록"""
        return [
            "python", "javascript", "typescript", "java", "cpp", "c",
            "csharp", "go", "rust", "php", "ruby", "swift", "kotlin",
            "scala", "r", "matlab", "sql", "html", "css", "xml", "yaml",
            "json", "markdown", "bash", "powershell"
        ]
    
    def get_diagram_types(self) -> list:
        """지원하는 다이어그램 타입 목록"""
        return [
            "flowchart", "sequence", "class", "state", "er", "user-journey",
            "gantt", "pie", "gitgraph", "mindmap", "timeline", "sankey-beta"
        ]
    
    def validate_language(self, language: str) -> bool:
        """프로그래밍 언어 유효성 검사"""
        return language.lower() in [lang.lower() for lang in self.get_supported_languages()]
    
    def get_default_language(self) -> str:
        """기본 프로그래밍 언어 반환"""
        return "python"
