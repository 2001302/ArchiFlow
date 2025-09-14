"""
응답 후처리 모듈
AI 응답을 적절한 형식으로 정리하고 포맷팅합니다.
"""
from ..models.enums import OutputFormat

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
