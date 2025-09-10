"""
프롬프트 템플릿 관리 모듈
다양한 출력 형식에 맞는 프롬프트 템플릿을 제공합니다.
"""
from typing import Dict, Any
from enum import Enum

class PromptType(Enum):
    """프롬프트 타입 열거형"""
    DIAGRAM_CREATE = "diagram_create"
    DIAGRAM_EDIT = "diagram_edit"
    SOURCE_CREATE = "source_create"
    SOURCE_EDIT = "source_edit"
    CHAT = "chat"

class PromptTemplates:
    """프롬프트 템플릿 클래스"""
    
    # Mermaid 다이어그램 생성 템플릿
    MERMAID_CREATE_TEMPLATE = """
다음 요청에 대해 Mermaid 다이어그램을 생성해주세요.

요청: {prompt}

소스코드 컨텍스트:
{source_code}

다이어그램 컨텍스트:
{diagram_context}

지침:
1. Mermaid 문법을 정확히 사용해주세요
2. 다이어그램은 명확하고 이해하기 쉽게 구성해주세요
3. 관계와 흐름을 명확히 표현해주세요
4. 답변은 반드시 ```mermaid로 시작하고 ```로 끝나는 코드 블록 형태로 제공해주세요

답변:
"""
    
    # Mermaid 다이어그램 편집 템플릿
    MERMAID_EDIT_TEMPLATE = """
다음 Mermaid 다이어그램을 편집해주세요.

기존 다이어그램:
{existing_diagram}

편집 요청: {prompt}

소스코드 컨텍스트:
{source_code}

다이어그램 컨텍스트:
{diagram_context}

지침:
1. 기존 다이어그램의 구조를 유지하면서 요청사항을 반영해주세요
2. Mermaid 문법을 정확히 사용해주세요
3. 답변은 반드시 ```mermaid로 시작하고 ```로 끝나는 코드 블록 형태로 제공해주세요

답변:
"""
    
    # 소스코드 생성 템플릿
    SOURCE_CREATE_TEMPLATE = """
다음 요청에 대해 {language} 소스코드를 생성해주세요.

요청: {prompt}

다이어그램 컨텍스트:
{diagram_context}

기존 소스코드:
{existing_source}

지침:
1. {language} 문법을 정확히 사용해주세요
2. 코드는 실행 가능하고 효율적이어야 합니다
3. 주석을 적절히 포함해주세요
4. 답변은 반드시 ```{language}로 시작하고 ```로 끝나는 코드 블록 형태로 제공해주세요

답변:
"""
    
    # 소스코드 편집 템플릿
    SOURCE_EDIT_TEMPLATE = """
다음 {language} 소스코드를 편집해주세요.

기존 소스코드:
{existing_source}

편집 요청: {prompt}

다이어그램 컨텍스트:
{diagram_context}

지침:
1. 기존 코드의 구조를 유지하면서 요청사항을 반영해주세요
2. {language} 문법을 정확히 사용해주세요
3. 코드는 실행 가능하고 효율적이어야 합니다
4. 답변은 반드시 ```{language}로 시작하고 ```로 끝나는 코드 블록 형태로 제공해주세요

답변:
"""
    
    # 일반 채팅 템플릿
    CHAT_TEMPLATE = """
다음 요청에 대해 도움을 드리겠습니다.

요청: {prompt}

소스코드 컨텍스트:
{source_code}

다이어그램 컨텍스트:
{diagram_context}

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
            PromptType.DIAGRAM_CREATE: cls.MERMAID_CREATE_TEMPLATE,
            PromptType.DIAGRAM_EDIT: cls.MERMAID_EDIT_TEMPLATE,
            PromptType.SOURCE_CREATE: cls.SOURCE_CREATE_TEMPLATE,
            PromptType.SOURCE_EDIT: cls.SOURCE_EDIT_TEMPLATE,
            PromptType.CHAT: cls.CHAT_TEMPLATE
        }
        return templates[prompt_type]
    
    @classmethod
    def format_prompt(
        cls,
        prompt_type: PromptType,
        prompt: str,
        source_code: str = "",
        diagram_context: str = "",
        existing_diagram: str = "",
        existing_source: str = "",
        language: str = "python"
    ) -> str:
        """프롬프트 포맷팅"""
        template = cls.get_template(prompt_type)
        
        return template.format(
            prompt=prompt,
            source_code=source_code or "없음",
            diagram_context=diagram_context or "없음",
            existing_diagram=existing_diagram or "없음",
            existing_source=existing_source or "없음",
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
    def get_diagram_types(cls) -> list:
        """지원하는 다이어그램 타입 목록"""
        return [
            "flowchart", "sequence", "class", "state", "er", "user-journey",
            "gantt", "pie", "gitgraph", "mindmap", "timeline", "sankey-beta"
        ]
