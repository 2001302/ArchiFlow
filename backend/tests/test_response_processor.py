"""
응답 후처리 유닛테스트
"""
import pytest
import sys
from pathlib import Path

# AI Core 모듈 경로 추가
mcp_server_path = Path(__file__).parent.parent / "mcp_server"
sys.path.insert(0, str(mcp_server_path))

from mcp_server.processors.response_processor import ResponseProcessor
from mcp_server.models.enums import OutputFormat

class TestResponseProcessor:
    """응답 후처리 테스트 클래스"""
    
    def setup_method(self):
        """테스트 설정"""
        self.processor = ResponseProcessor()
    
    def test_process_response_text_format(self):
        """텍스트 형식 응답 후처리 테스트"""
        response = "This is a test response"
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert isinstance(result, str)
    
    def test_process_response_document_format(self):
        """문서 형식 응답 후처리 테스트"""
        response = "This is a test document response"
        result = self.processor.process_response(response, OutputFormat.DOCUMENT)
        
        assert result == response
        assert isinstance(result, str)
    
    def test_process_response_empty_string(self):
        """빈 문자열 응답 후처리 테스트"""
        response = ""
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert result == ""
    
    def test_process_response_whitespace_string(self):
        """공백 문자열 응답 후처리 테스트"""
        response = "   \n\t   "
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert result == "   \n\t   "
    
    def test_process_response_multiline_string(self):
        """여러 줄 문자열 응답 후처리 테스트"""
        response = """Line 1
Line 2
Line 3"""
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result
    
    def test_process_response_special_characters(self):
        """특수 문자 포함 응답 후처리 테스트"""
        response = "Response with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert "!@#$%^&*()_+-=[]{}|;':\",./<>?" in result
    
    def test_process_response_unicode_characters(self):
        """유니코드 문자 포함 응답 후처리 테스트"""
        response = "Response with unicode: 안녕하세요 こんにちは 你好 🌟"
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert "안녕하세요" in result
        assert "こんにちは" in result
        assert "你好" in result
        assert "🌟" in result
    
    def test_process_response_json_like_string(self):
        """JSON 형태 문자열 응답 후처리 테스트"""
        response = '{"key": "value", "number": 123, "boolean": true}'
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert '{"key": "value"' in result
    
    def test_process_response_markdown_string(self):
        """마크다운 형태 문자열 응답 후처리 테스트"""
        response = """# Title
## Subtitle
- Item 1
- Item 2
**Bold text** and *italic text*"""
        result = self.processor.process_response(response, OutputFormat.DOCUMENT)
        
        assert result == response
        assert "# Title" in result
        assert "## Subtitle" in result
        assert "- Item 1" in result
        assert "**Bold text**" in result
        assert "*italic text*" in result
    
    def test_process_response_html_like_string(self):
        """HTML 형태 문자열 응답 후처리 테스트"""
        response = "<h1>Title</h1><p>Paragraph with <strong>bold</strong> text.</p>"
        result = self.processor.process_response(response, OutputFormat.DOCUMENT)
        
        assert result == response
        assert "<h1>Title</h1>" in result
        assert "<p>Paragraph" in result
        assert "<strong>bold</strong>" in result
    
    def test_process_response_code_block_string(self):
        """코드 블록 형태 문자열 응답 후처리 테스트"""
        response = """```python
def hello_world():
    print("Hello, World!")
```"""
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert "```python" in result
        assert "def hello_world():" in result
        assert 'print("Hello, World!")' in result
        assert "```" in result
    
    def test_process_response_none_input(self):
        """None 입력 응답 후처리 테스트"""
        response = None
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result is None
    
    def test_process_response_numeric_input(self):
        """숫자 입력 응답 후처리 테스트"""
        response = 12345
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == 12345
        assert isinstance(result, int)
    
    def test_process_response_list_input(self):
        """리스트 입력 응답 후처리 테스트"""
        response = ["item1", "item2", "item3"]
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert isinstance(result, list)
        assert len(result) == 3
        assert "item1" in result
        assert "item2" in result
        assert "item3" in result
    
    def test_process_response_dict_input(self):
        """딕셔너리 입력 응답 후처리 테스트"""
        response = {"key1": "value1", "key2": "value2"}
        result = self.processor.process_response(response, OutputFormat.TEXT)
        
        assert result == response
        assert isinstance(result, dict)
        assert result["key1"] == "value1"
        assert result["key2"] == "value2"
