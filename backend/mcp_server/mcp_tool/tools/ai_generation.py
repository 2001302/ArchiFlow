"""
AI 생성 도구들
텍스트 생성, 문서 생성, 요약 등 AI 관련 기능
"""
import asyncio
import json
from typing import Dict, Any, Optional
from loguru import logger

from ...managers.mcp_engine import MCPEngine
from ...models.enums import AIProvider, OutputFormat

class AIGenerationTools:
    """AI 생성 도구 클래스"""
    
    def __init__(self):
        self.mcp_engine = MCPEngine()
    
    async def generate_text(
        self, 
        prompt: str, 
        provider: str = "perplexity",
        model: str = "gpt-4",
        api_key: Optional[str] = None
    ) -> str:
        """
        일반 텍스트 생성
        
        Args:
            prompt: 생성할 텍스트에 대한 프롬프트
            provider: AI 제공자 (perplexity, openai, anthropic)
            model: 사용할 모델
            api_key: API 키 (선택사항)
        
        Returns:
            생성된 텍스트
        """
        try:
            # AI 제공자 설정
            provider_enum = AIProvider.PERPLEXITY
            if provider.lower() == "openai":
                provider_enum = AIProvider.OPENAI
            elif provider.lower() == "anthropic":
                provider_enum = AIProvider.ANTHROPIC
            
            # MCP 엔진을 통한 텍스트 생성
            response = await self.mcp_engine.generate_response(
                prompt=prompt,
                output_format=OutputFormat.TEXT,
                provider=provider_enum,
                model=model,
                api_key=api_key
            )
            
            # 응답에서 텍스트 추출
            if response.get("success"):
                result = response.get("data", {}).get("content", "")
            else:
                result = f"AI 생성 실패: {response.get('error', '알 수 없는 오류')}"
            
            return result
            
        except Exception as e:
            logger.error(f"텍스트 생성 실패: {str(e)}")
            return f"텍스트 생성 중 오류가 발생했습니다: {str(e)}"
    
    async def generate_document(
        self, 
        prompt: str, 
        language: str = "python",
        provider: str = "perplexity",
        api_key: Optional[str] = None
    ) -> str:
        """
        구조화된 문서 생성
        
        Args:
            prompt: 생성할 문서에 대한 프롬프트
            language: 프로그래밍 언어
            provider: AI 제공자
            api_key: API 키 (선택사항)
        
        Returns:
            생성된 문서
        """
        try:
            # 문서 생성용 프롬프트 구성
            document_prompt = f"""
다음 요구사항에 따라 {language} 코드를 생성해주세요:

{prompt}

요구사항:
1. 완전하고 실행 가능한 코드를 작성해주세요
2. 적절한 주석을 포함해주세요
3. 에러 처리를 포함해주세요
4. 코드 블록으로 감싸서 반환해주세요
"""
            
            result = await self.generate_text(
                prompt=document_prompt,
                provider=provider,
                api_key=api_key
            )
            
            return result
            
        except Exception as e:
            logger.error(f"문서 생성 실패: {str(e)}")
            return f"문서 생성 중 오류가 발생했습니다: {str(e)}"
    
    async def summarize_content(
        self, 
        content: str, 
        max_length: int = 200,
        provider: str = "perplexity"
    ) -> str:
        """
        콘텐츠 요약
        
        Args:
            content: 요약할 콘텐츠
            max_length: 최대 길이
            provider: AI 제공자
        
        Returns:
            요약된 콘텐츠
        """
        try:
            # 요약용 프롬프트 구성
            summary_prompt = f"""
다음 콘텐츠를 {max_length}자 이내로 요약해주세요:

{content}

요약 요구사항:
1. 핵심 내용을 간결하게 정리해주세요
2. 중요한 키워드와 개념을 포함해주세요
3. 원문의 의미를 왜곡하지 않도록 주의해주세요
"""
            
            result = await self.generate_text(
                prompt=summary_prompt,
                provider=provider
            )
            
            return result
            
        except Exception as e:
            logger.error(f"콘텐츠 요약 실패: {str(e)}")
            return f"콘텐츠 요약 중 오류가 발생했습니다: {str(e)}"
    
    async def generate_code_explanation(
        self, 
        code: str, 
        language: str = "python",
        provider: str = "perplexity"
    ) -> str:
        """
        코드 설명 생성
        
        Args:
            code: 설명할 코드
            language: 프로그래밍 언어
            provider: AI 제공자
        
        Returns:
            코드 설명
        """
        try:
            explanation_prompt = f"""
다음 {language} 코드를 자세히 설명해주세요:

```{language}
{code}
```

설명 요구사항:
1. 코드의 전체적인 목적과 기능을 설명해주세요
2. 각 부분별로 상세한 설명을 제공해주세요
3. 사용된 알고리즘이나 패턴이 있다면 설명해주세요
4. 실행 결과나 예상 동작을 설명해주세요
"""
            
            result = await self.generate_text(
                prompt=explanation_prompt,
                provider=provider
            )
            
            return result
            
        except Exception as e:
            logger.error(f"코드 설명 생성 실패: {str(e)}")
            return f"코드 설명 생성 중 오류가 발생했습니다: {str(e)}"
    
    async def generate_documentation(
        self, 
        code: str, 
        language: str = "python",
        style: str = "docstring",
        provider: str = "perplexity"
    ) -> str:
        """
        코드 문서화 생성
        
        Args:
            code: 문서화할 코드
            language: 프로그래밍 언어
            style: 문서화 스타일 (docstring, markdown, etc.)
            provider: AI 제공자
        
        Returns:
            생성된 문서
        """
        try:
            doc_prompt = f"""
다음 {language} 코드에 대한 {style} 스타일의 문서를 생성해주세요:

```{language}
{code}
```

문서화 요구사항:
1. 함수/클래스의 목적과 기능을 명확히 설명해주세요
2. 매개변수와 반환값을 상세히 설명해주세요
3. 사용 예제를 포함해주세요
4. 주의사항이나 제한사항이 있다면 명시해주세요
5. {style} 형식에 맞게 작성해주세요
"""
            
            result = await self.generate_text(
                prompt=doc_prompt,
                provider=provider
            )
            
            return result
            
        except Exception as e:
            logger.error(f"문서화 생성 실패: {str(e)}")
            return f"문서화 생성 중 오류가 발생했습니다: {str(e)}"