"""
옵시디언 볼트 관리자
볼트 파일 시스템 조작을 담당합니다.
"""
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger
import aiofiles
import re


class VaultManager:
    """옵시디언 볼트 관리자"""
    
    def __init__(self, vault_path: Optional[str] = None):
        self.vault_path = Path(vault_path) if vault_path else None
        self.supported_extensions = {'.md', '.txt', '.json', '.yaml', '.yml'}
    
    def set_vault_path(self, vault_path: str):
        """볼트 경로 설정"""
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"볼트 경로가 존재하지 않습니다: {vault_path}")
    
    async def read_note(self, note_path: str) -> Optional[str]:
        """노트 읽기"""
        try:
            full_path = self._get_full_path(note_path)
            if not full_path.exists():
                return None
            
            async with aiofiles.open(full_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                return content
                
        except Exception as e:
            logger.error(f"노트 읽기 실패: {str(e)}")
            return None
    
    async def write_note(self, note_path: str, content: str) -> bool:
        """노트 쓰기"""
        try:
            full_path = self._get_full_path(note_path)
            
            # 디렉토리 생성
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
                await f.write(content)
                return True
                
        except Exception as e:
            logger.error(f"노트 쓰기 실패: {str(e)}")
            return False
    
    async def create_note(self, note_path: str, content: str = "") -> bool:
        """새 노트 생성"""
        try:
            full_path = self._get_full_path(note_path)
            
            if full_path.exists():
                return False  # 이미 존재하는 파일
            
            # 디렉토리 생성
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(full_path, 'w', encoding='utf-8') as f:
                await f.write(content)
                return True
                
        except Exception as e:
            logger.error(f"노트 생성 실패: {str(e)}")
            return False
    
    async def delete_note(self, note_path: str) -> bool:
        """노트 삭제"""
        try:
            full_path = self._get_full_path(note_path)
            
            if not full_path.exists():
                return False
            
            full_path.unlink()
            return True
            
        except Exception as e:
            logger.error(f"노트 삭제 실패: {str(e)}")
            return False
    
    async def list_notes(self, directory: str = "", recursive: bool = True) -> List[Dict[str, Any]]:
        """노트 목록 조회"""
        try:
            search_path = self._get_full_path(directory) if directory else self.vault_path
            
            if not search_path.exists():
                return []
            
            notes = []
            
            if recursive:
                for file_path in search_path.rglob("*"):
                    if file_path.is_file() and file_path.suffix in self.supported_extensions:
                        relative_path = file_path.relative_to(self.vault_path)
                        notes.append({
                            "path": str(relative_path),
                            "name": file_path.stem,
                            "extension": file_path.suffix,
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime
                        })
            else:
                for file_path in search_path.iterdir():
                    if file_path.is_file() and file_path.suffix in self.supported_extensions:
                        relative_path = file_path.relative_to(self.vault_path)
                        notes.append({
                            "path": str(relative_path),
                            "name": file_path.stem,
                            "extension": file_path.suffix,
                            "size": file_path.stat().st_size,
                            "modified": file_path.stat().st_mtime
                        })
            
            return notes
            
        except Exception as e:
            logger.error(f"노트 목록 조회 실패: {str(e)}")
            return []
    
    async def search_notes(
        self, 
        query: str, 
        search_type: str = "content", 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """노트 검색"""
        try:
            notes = await self.list_notes(recursive=True)
            results = []
            
            for note in notes:
                if len(results) >= limit:
                    break
                
                note_content = await self.read_note(note["path"])
                if not note_content:
                    continue
                
                match = False
                
                if search_type == "content":
                    # 내용 검색
                    if query.lower() in note_content.lower():
                        match = True
                elif search_type == "title":
                    # 제목 검색
                    if query.lower() in note["name"].lower():
                        match = True
                elif search_type == "tag":
                    # 태그 검색
                    tags = re.findall(r'#\w+', note_content)
                    if any(query.lower() in tag.lower() for tag in tags):
                        match = True
                elif search_type == "link":
                    # 링크 검색
                    links = re.findall(r'\[\[([^\]]+)\]\]', note_content)
                    if any(query.lower() in link.lower() for link in links):
                        match = True
                
                if match:
                    # 검색 결과에 컨텍스트 추가
                    context = self._extract_context(note_content, query)
                    results.append({
                        **note,
                        "context": context,
                        "match_type": search_type
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"노트 검색 실패: {str(e)}")
            return []
    
    async def get_vault_structure(self) -> Dict[str, Any]:
        """볼트 구조 조회"""
        try:
            if not self.vault_path or not self.vault_path.exists():
                return {"error": "볼트 경로가 설정되지 않았거나 존재하지 않습니다."}
            
            structure = {
                "vault_path": str(self.vault_path),
                "total_notes": 0,
                "directories": {},
                "files": []
            }
            
            # 디렉토리 구조 생성
            for item in self.vault_path.rglob("*"):
                if item.is_file() and item.suffix in self.supported_extensions:
                    structure["total_notes"] += 1
                    
                    relative_path = item.relative_to(self.vault_path)
                    path_parts = relative_path.parts
                    
                    # 디렉토리 구조에 추가
                    current = structure["directories"]
                    for part in path_parts[:-1]:  # 파일명 제외
                        if part not in current:
                            current[part] = {"type": "directory", "children": {}}
                        current = current[part]["children"]
                    
                    # 파일 정보 추가
                    file_info = {
                        "name": item.name,
                        "path": str(relative_path),
                        "size": item.stat().st_size,
                        "modified": item.stat().st_mtime
                    }
                    structure["files"].append(file_info)
            
            return structure
            
        except Exception as e:
            logger.error(f"볼트 구조 조회 실패: {str(e)}")
            return {"error": str(e)}
    
    def _get_full_path(self, note_path: str) -> Path:
        """전체 경로 생성"""
        if not self.vault_path:
            raise ValueError("볼트 경로가 설정되지 않았습니다.")
        
        # 절대 경로인 경우 그대로 사용
        if os.path.isabs(note_path):
            return Path(note_path)
        
        # 상대 경로인 경우 볼트 경로 기준으로 생성
        return self.vault_path / note_path
    
    def _extract_context(self, content: str, query: str, context_length: int = 100) -> str:
        """검색 결과 컨텍스트 추출"""
        query_lower = query.lower()
        content_lower = content.lower()
        
        # 쿼리가 포함된 위치 찾기
        match_index = content_lower.find(query_lower)
        if match_index == -1:
            return content[:context_length] + "..." if len(content) > context_length else content
        
        # 컨텍스트 시작과 끝 계산
        start = max(0, match_index - context_length // 2)
        end = min(len(content), match_index + len(query) + context_length // 2)
        
        context = content[start:end]
        
        # 앞뒤에 ... 추가
        if start > 0:
            context = "..." + context
        if end < len(content):
            context = context + "..."
        
        return context
