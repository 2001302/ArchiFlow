"""
프롬프트 템플릿 관리 모듈
다양한 출력 형식에 맞는 프롬프트 템플릿을 제공합니다.
"""
from typing import Dict, Any
from enum import Enum

class PromptType(Enum):
    """프롬프트 타입 열거형"""
    DOCUMENT_CREATE = "document_create"
    DOCUMENT_EDIT = "document_edit"
    CHAT = "chat"

class PromptTemplates:
    """프롬프트 템플릿 클래스"""
    
    # 문서 생성 템플릿
    DOCUMENT_CREATE_TEMPLATE = """
다음 요청에 대해 포괄적인 문서를 생성해주세요.

요청: {prompt}

지침:
1. 명확한 섹션과 구조를 가진 문서를 작성해주세요
2. 적절한 제목과 포맷팅을 사용해주세요
3. 관련 예시와 설명을 포함해주세요
4. 내용을 이해하기 쉽고 유익하게 만들어주세요
5. 한국어로 답변해주세요

답변:
"""
    
    # 문서 편집 템플릿
    DOCUMENT_EDIT_TEMPLATE = """
다음 문서를 편집해주세요.

기존 문서:
{existing_document}

편집 요청: {prompt}

지침:
1. 기존 문서의 구조를 유지하면서 요청사항을 반영해주세요
2. 명확한 섹션과 구조를 유지해주세요
3. 적절한 제목과 포맷팅을 사용해주세요
4. 내용을 이해하기 쉽고 유익하게 만들어주세요
5. 한국어로 답변해주세요

답변:
"""
    
    # 일반 채팅 템플릿
    CHAT_TEMPLATE = """
다음 요청에 대해 도움을 드리겠습니다.

요청: {prompt}

지침:
1. 정확하고 유용한 정보를 제공해주세요
2. 필요시 예시나 설명을 포함해주세요
3. 한국어로 답변해주세요

답변:
"""
    
    @classmethod
    def get_template(cls, prompt_type: PromptType) -> str:
        """프롬프트 템플릿 반환"""
        templates = {
            PromptType.DOCUMENT_CREATE: cls.DOCUMENT_CREATE_TEMPLATE,
            PromptType.DOCUMENT_EDIT: cls.DOCUMENT_EDIT_TEMPLATE,
            PromptType.CHAT: cls.CHAT_TEMPLATE
        }
        return templates[prompt_type]
    
    @classmethod
    def format_prompt(
        cls,
        prompt_type: PromptType,
        prompt: str,
        existing_document: str = "",
        language: str = "python"
    ) -> str:
        """프롬프트 포맷팅"""
        template = cls.get_template(prompt_type)
        
        return template.format(
            prompt=prompt,
            existing_document=existing_document or "없음",
            language=language
        )
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """지원하는 프로그래밍 언어 목록"""
        return [
            "python", "javascript", "typescript", "java", "cpp", "c",
            "csharp", "go", "rust", "php", "ruby", "swift", "kotlin",
            "scala", "r", "matlab", "sql", "html", "css", "xml", "yaml",
            "json", "markdown", "bash", "powershell"
        ]
    
    @classmethod
    def get_document_types(cls) -> list:
        """지원하는 문서 타입 목록"""
        return [
            "technical_document", "user_manual", "api_documentation", 
            "tutorial", "guide", "reference", "specification", "report"
        ]
