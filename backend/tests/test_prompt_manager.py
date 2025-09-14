"""
프롬프트 매니저 유닛테스트
"""
import pytest
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
mcp_server_path = Path(__file__).parent.parent / "mcp_server"
sys.path.insert(0, str(mcp_server_path))

from mcp_server.managers.prompt_manager import PromptManager
from mcp_server.models.enums import OutputFormat

class TestPromptManager:
    """프롬프트 매니저 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.prompt_manager = PromptManager()
    
    def test_format_prompt_text(self):
        """텍스트 형식 프롬프트 포맷팅 테스트"""
        result = self.prompt_manager.format_prompt(
            prompt="Test prompt",
            output_format=OutputFormat.TEXT,
            language="python"
        )
        
        assert "Test prompt" in result
        assert "python" in result
        assert "Please help with the following request" in result
    
    def test_format_prompt_document(self):
        """문서 형식 프롬프트 포맷팅 테스트"""
        result = self.prompt_manager.format_prompt(
            prompt="Test document prompt",
            output_format=OutputFormat.DOCUMENT,
            language="javascript"
        )
        
        assert "Test document prompt" in result
        assert "javascript" in result
        assert "Please create a comprehensive document" in result
    
    def test_format_prompt_no_language(self):
        """언어 미지정 프롬프트 포맷팅 테스트"""
        result = self.prompt_manager.format_prompt(
            prompt="Test prompt",
            output_format=OutputFormat.TEXT
        )
        
        assert "Test prompt" in result
        assert "python" in result  # 기본 언어
    
    def test_get_supported_languages(self):
        """지원 언어 목록 테스트"""
        languages = self.prompt_manager.get_supported_languages()
        
        assert isinstance(languages, list)
        assert "python" in languages
        assert "javascript" in languages
        assert "typescript" in languages
        assert "java" in languages
        assert "cpp" in languages
        assert "c" in languages
        assert "csharp" in languages
        assert "go" in languages
        assert "rust" in languages
        assert "php" in languages
        assert "ruby" in languages
        assert "swift" in languages
        assert "kotlin" in languages
        assert "scala" in languages
        assert "r" in languages
        assert "matlab" in languages
        assert "sql" in languages
        assert "html" in languages
        assert "css" in languages
        assert "xml" in languages
        assert "yaml" in languages
        assert "json" in languages
        assert "markdown" in languages
        assert "bash" in languages
        assert "powershell" in languages
    
    def test_get_document_types(self):
        """지원 문서 타입 목록 테스트"""
        doc_types = self.prompt_manager.get_document_types()
        
        assert isinstance(doc_types, list)
        assert "technical_document" in doc_types
        assert "user_manual" in doc_types
        assert "api_documentation" in doc_types
        assert "tutorial" in doc_types
        assert "guide" in doc_types
        assert "reference" in doc_types
        assert "specification" in doc_types
        assert "report" in doc_types
    
    def test_validate_language_valid(self):
        """유효한 언어 검증 테스트"""
        assert self.prompt_manager.validate_language("python") is True
        assert self.prompt_manager.validate_language("Python") is True
        assert self.prompt_manager.validate_language("PYTHON") is True
        assert self.prompt_manager.validate_language("javascript") is True
        assert self.prompt_manager.validate_language("JavaScript") is True
        assert self.prompt_manager.validate_language("JAVASCRIPT") is True
        assert self.prompt_manager.validate_language("typescript") is True
        assert self.prompt_manager.validate_language("java") is True
        assert self.prompt_manager.validate_language("cpp") is True
        assert self.prompt_manager.validate_language("c") is True
        assert self.prompt_manager.validate_language("csharp") is True
        assert self.prompt_manager.validate_language("go") is True
        assert self.prompt_manager.validate_language("rust") is True
        assert self.prompt_manager.validate_language("php") is True
        assert self.prompt_manager.validate_language("ruby") is True
        assert self.prompt_manager.validate_language("swift") is True
        assert self.prompt_manager.validate_language("kotlin") is True
        assert self.prompt_manager.validate_language("scala") is True
        assert self.prompt_manager.validate_language("r") is True
        assert self.prompt_manager.validate_language("matlab") is True
        assert self.prompt_manager.validate_language("sql") is True
        assert self.prompt_manager.validate_language("html") is True
        assert self.prompt_manager.validate_language("css") is True
        assert self.prompt_manager.validate_language("xml") is True
        assert self.prompt_manager.validate_language("yaml") is True
        assert self.prompt_manager.validate_language("json") is True
        assert self.prompt_manager.validate_language("markdown") is True
        assert self.prompt_manager.validate_language("bash") is True
        assert self.prompt_manager.validate_language("powershell") is True
    
    def test_validate_language_invalid(self):
        """유효하지 않은 언어 검증 테스트"""
        assert self.prompt_manager.validate_language("invalid_language") is False
        assert self.prompt_manager.validate_language("") is False
        assert self.prompt_manager.validate_language("123") is False
        assert self.prompt_manager.validate_language("python3") is False
        assert self.prompt_manager.validate_language("js") is False
        assert self.prompt_manager.validate_language("py") is False
        assert self.prompt_manager.validate_language("c++") is False
        assert self.prompt_manager.validate_language("c#") is False
    
    def test_get_default_language(self):
        """기본 언어 반환 테스트"""
        default_lang = self.prompt_manager.get_default_language()
        assert default_lang == "python"
    
    def test_text_template_content(self):
        """텍스트 템플릿 내용 테스트"""
        template = self.prompt_manager._get_text_template()
        
        assert "Please help with the following request" in template
        assert "Request: {prompt}" in template
        assert "Instructions:" in template
        assert "Provide accurate and useful information" in template
        assert "Include examples or explanations when necessary" in template
        assert "Respond in Korean" in template
        assert "Answer:" in template
    
    def test_document_template_content(self):
        """문서 템플릿 내용 테스트"""
        template = self.prompt_manager._get_document_template()
        
        assert "Please create a comprehensive document" in template
        assert "Request: {prompt}" in template
        assert "Instructions:" in template
        assert "Create a well-structured document" in template
        assert "Use appropriate headings and formatting" in template
        assert "Include relevant examples and explanations" in template
        assert "Make the content informative and easy to understand" in template
        assert "Respond in Korean" in template
        assert "Answer:" in template
    
    def test_format_prompt_with_special_characters(self):
        """특수 문자 포함 프롬프트 포맷팅 테스트"""
        special_prompt = "Test prompt with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.prompt_manager.format_prompt(
            prompt=special_prompt,
            output_format=OutputFormat.TEXT,
            language="python"
        )
        
        assert special_prompt in result
        assert "python" in result
    
    def test_format_prompt_empty_prompt(self):
        """빈 프롬프트 포맷팅 테스트"""
        result = self.prompt_manager.format_prompt(
            prompt="",
            output_format=OutputFormat.TEXT,
            language="python"
        )
        
        assert "" in result
        assert "python" in result
