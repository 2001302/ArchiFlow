"""
옵시디언 특화 MCP 엔진
MCPEngine을 상속받아 옵시디언 볼트 조작 기능을 추가합니다.
"""
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
from loguru import logger

# MCP Server에서 상속
import sys
from pathlib import Path as PathLib
mcp_server_path = PathLib(__file__).parent.parent.parent / "mcp_server"
sys.path.insert(0, str(mcp_server_path))

from mcp_server.managers.mcp_engine import MCPEngine
from mcp_server.models.enums import OutputFormat, AIProvider

from ..tools.vault_manager import VaultManager
from ..tools.note_processor import NoteProcessor
from ..config.obsidian_settings import ObsidianSettings


class ObsidianEngine(MCPEngine):
    """옵시디언 특화 MCP 엔진"""
    
    def __init__(self, vault_path: Optional[str] = None):
        super().__init__()
        self.vault_manager = VaultManager(vault_path)
        self.note_processor = NoteProcessor()
        self.obsidian_settings = ObsidianSettings()
    
    async def generate_response(
        self,
        prompt: str,
        output_format: OutputFormat,
        provider: AIProvider = AIProvider.PERPLEXITY,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        language: Optional[str] = None,
        vault_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        옵시디언 컨텍스트를 포함한 AI 응답 생성
        
        Args:
            prompt: 사용자 프롬프트
            output_format: 출력 형식
            provider: AI 제공자
            model: 모델명
            api_key: API 키
            language: 프로그래밍 언어
            vault_context: 볼트 컨텍스트 정보
        
        Returns:
            AI 응답 딕셔너리
        """
        try:
            # 볼트 컨텍스트가 제공된 경우 프롬프트에 추가
            if vault_context:
                enhanced_prompt = self._enhance_prompt_with_vault_context(prompt, vault_context)
            else:
                enhanced_prompt = prompt
            
            # 부모 클래스의 generate_response 호출
            result = await super().generate_response(
                prompt=enhanced_prompt,
                output_format=output_format,
                provider=provider,
                model=model,
                api_key=api_key,
                language=language
            )
            
            return result
            
        except Exception as e:
            logger.error(f"옵시디언 AI 응답 생성 실패: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider.value,
                "output_format": output_format.value
            }
    
    def _enhance_prompt_with_vault_context(self, prompt: str, vault_context: Dict[str, Any]) -> str:
        """볼트 컨텍스트로 프롬프트 강화"""
        context_info = []
        
        if "current_note" in vault_context:
            context_info.append(f"현재 노트: {vault_context['current_note']}")
        
        if "related_notes" in vault_context:
            context_info.append(f"관련 노트들: {', '.join(vault_context['related_notes'])}")
        
        if "vault_structure" in vault_context:
            context_info.append(f"볼트 구조: {vault_context['vault_structure']}")
        
        if context_info:
            enhanced_prompt = f"""
볼트 컨텍스트:
{chr(10).join(context_info)}

사용자 요청:
{prompt}
"""
            return enhanced_prompt
        
        return prompt
    
    async def process_note_with_ai(
        self,
        note_path: str,
        operation: str,
        prompt: str,
        provider: AIProvider = AIProvider.PERPLEXITY,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        노트를 AI로 처리
        
        Args:
            note_path: 노트 파일 경로
            operation: 처리 작업 (summarize, enhance, generate_outline 등)
            prompt: AI 프롬프트
            provider: AI 제공자
            api_key: API 키
        
        Returns:
            처리 결과
        """
        try:
            # 노트 읽기
            note_content = await self.vault_manager.read_note(note_path)
            if not note_content:
                return {"success": False, "error": "노트를 읽을 수 없습니다."}
            
            # 작업별 프롬프트 생성
            operation_prompt = self._create_operation_prompt(operation, prompt, note_content)
            
            # AI 응답 생성
            result = await self.generate_response(
                prompt=operation_prompt,
                output_format=OutputFormat.TEXT,
                provider=provider,
                api_key=api_key
            )
            
            if result.get("success"):
                # 결과를 노트에 적용
                processed_content = self.note_processor.apply_ai_result(
                    note_content, result["content"], operation
                )
                
                # 노트 저장
                await self.vault_manager.write_note(note_path, processed_content)
                
                return {
                    "success": True,
                    "operation": operation,
                    "note_path": note_path,
                    "ai_result": result["content"]
                }
            else:
                return result
                
        except Exception as e:
            logger.error(f"노트 AI 처리 실패: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _create_operation_prompt(self, operation: str, user_prompt: str, note_content: str) -> str:
        """작업별 프롬프트 생성"""
        operation_templates = {
            "summarize": f"다음 노트의 내용을 요약해주세요:\n\n{note_content}\n\n추가 요청: {user_prompt}",
            "enhance": f"다음 노트의 내용을 개선하고 보완해주세요:\n\n{note_content}\n\n개선 요청: {user_prompt}",
            "generate_outline": f"다음 노트의 내용을 바탕으로 목차를 생성해주세요:\n\n{note_content}\n\n목차 요청: {user_prompt}",
            "translate": f"다음 노트를 번역해주세요:\n\n{note_content}\n\n번역 요청: {user_prompt}",
            "format": f"다음 노트의 형식을 개선해주세요:\n\n{note_content}\n\n형식 요청: {user_prompt}"
        }
        
        return operation_templates.get(operation, f"{operation} 작업을 수행해주세요:\n\n{note_content}\n\n요청: {user_prompt}")
    
    async def search_vault(
        self,
        query: str,
        search_type: str = "content",
        limit: int = 10
    ) -> Dict[str, Any]:
        """볼트 검색"""
        try:
            results = await self.vault_manager.search_notes(query, search_type, limit)
            return {
                "success": True,
                "query": query,
                "search_type": search_type,
                "results": results
            }
        except Exception as e:
            logger.error(f"볼트 검색 실패: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def get_vault_structure(self) -> Dict[str, Any]:
        """볼트 구조 조회"""
        try:
            structure = await self.vault_manager.get_vault_structure()
            return {
                "success": True,
                "structure": structure
            }
        except Exception as e:
            logger.error(f"볼트 구조 조회 실패: {str(e)}")
            return {"success": False, "error": str(e)}
