"""
프롬프트 매니저 모듈
다양한 출력 형식에 맞는 프롬프트 템플릿을 관리합니다.
"""
from typing import Optional
from ..models.enums import OutputFormat

class PromptManager:
    """프롬프트 매니저 클래스"""
    
    def format_prompt(
        self,
        prompt: str,
        output_format: OutputFormat,
        language: Optional[str] = None
    ) -> str:
        """
        프롬프트 포맷팅
        
        Args:
            prompt: 사용자 프롬프트
            output_format: 출력 형식
            language: 프로그래밍 언어
        
        Returns:
            포맷된 프롬프트
        """
        templates = {
            OutputFormat.TEXT: self._get_text_template(),
            OutputFormat.DOCUMENT: self._get_document_template()
        }
        
        template = templates[output_format]
        return template.format(
            prompt=prompt,
            language=language or "python"
        )
    
    def _get_document_template(self) -> str:
        """문서 생성 템플릿"""
        return """
Please create a comprehensive document based on the following request.

Request: {prompt}

Instructions:
1. Create a well-structured document with clear sections
2. Use appropriate headings and formatting
3. Include relevant examples and explanations
4. Make the content informative and easy to understand
5. Respond in Korean
6. Use {language} programming language if applicable

Answer:
"""
    
    def _get_text_template(self) -> str:
        """일반 텍스트 템플릿"""
        return """
Please help with the following request.

Request: {prompt}

Instructions:
1. Provide accurate and useful information
2. Include examples or explanations when necessary
3. Respond in Korean
4. Use {language} programming language if applicable

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
    
    def get_document_types(self) -> list:
        """지원하는 문서 타입 목록"""
        return [
            "technical_document", "user_manual", "api_documentation", 
            "tutorial", "guide", "reference", "specification", "report"
        ]
    
    def validate_language(self, language: str) -> bool:
        """프로그래밍 언어 유효성 검사"""
        return language.lower() in [lang.lower() for lang in self.get_supported_languages()]
    
    def get_default_language(self) -> str:
        """기본 프로그래밍 언어 반환"""
        return "python"
