"""
볼트 조작 도구들
옵시디언 볼트 파일 시스템 접근 및 조작
"""
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

class VaultOperationTools:
    """볼트 조작 도구 클래스"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"볼트 경로가 존재하지 않습니다: {vault_path}")
    
    def list_vault_files(
        self, 
        pattern: str = "*.md", 
        recursive: bool = True
    ) -> List[Dict[str, Any]]:
        """
        볼트 내 파일 목록 조회
        
        Args:
            pattern: 파일 패턴 (예: *.md, *.txt)
            recursive: 재귀적 검색 여부
        
        Returns:
            파일 정보 목록
        """
        try:
            files = []
            search_pattern = "**/" + pattern if recursive else pattern
            
            for file_path in self.vault_path.glob(search_pattern):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        "name": file_path.name,
                        "path": str(file_path.relative_to(self.vault_path)),
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "extension": file_path.suffix,
                        "is_markdown": file_path.suffix.lower() == '.md'
                    })
            
            return sorted(files, key=lambda x: x["modified"], reverse=True)
            
        except Exception as e:
            logger.error(f"파일 목록 조회 실패: {str(e)}")
            return []
    
    def read_file_content(self, file_path: str) -> str:
        """
        파일 내용 읽기
        
        Args:
            file_path: 읽을 파일 경로 (볼트 기준 상대 경로)
        
        Returns:
            파일 내용
        """
        try:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                return f"파일을 찾을 수 없습니다: {file_path}"
            
            content = full_path.read_text(encoding='utf-8')
            return content
            
        except Exception as e:
            logger.error(f"파일 읽기 실패: {str(e)}")
            return f"파일 읽기 중 오류 발생: {str(e)}"
    
    def create_note(
        self, 
        title: str, 
        content: str, 
        folder: str = "", 
        tags: List[str] = None
    ) -> str:
        """
        새 노트 생성
        
        Args:
            title: 노트 제목
            content: 노트 내용
            folder: 저장할 폴더 (선택사항)
            tags: 태그 목록 (선택사항)
        
        Returns:
            생성된 파일 경로
        """
        try:
            # 파일명 생성 (제목에서 안전한 파일명으로 변환)
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
            safe_title = safe_title.strip()
            
            if not safe_title:
                safe_title = "untitled"
            
            # 폴더 경로 설정
            if folder:
                folder_path = self.vault_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                file_path = folder_path / f"{safe_title}.md"
            else:
                file_path = self.vault_path / f"{safe_title}.md"
            
            # 중복 파일명 처리
            counter = 1
            original_path = file_path
            while file_path.exists():
                file_path = original_path.parent / f"{safe_title}_{counter}.md"
                counter += 1
            
            # 태그 추가
            if tags:
                tag_line = " ".join([f"#{tag}" for tag in tags])
                content = f"{tag_line}\n\n{content}"
            
            # 파일 생성
            file_path.write_text(content, encoding='utf-8')
            
            return str(file_path.relative_to(self.vault_path))
            
        except Exception as e:
            logger.error(f"노트 생성 실패: {str(e)}")
            return f"노트 생성 중 오류 발생: {str(e)}"
    
    def update_note(
        self, 
        file_path: str, 
        content: str, 
        append: bool = False
    ) -> str:
        """
        기존 노트 업데이트
        
        Args:
            file_path: 업데이트할 파일 경로
            content: 새로운 내용
            append: 기존 내용에 추가할지 여부
        
        Returns:
            업데이트 결과 메시지
        """
        try:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                return f"파일을 찾을 수 없습니다: {file_path}"
            
            if append:
                existing_content = full_path.read_text(encoding='utf-8')
                new_content = existing_content + "\n\n" + content
            else:
                new_content = content
            
            full_path.write_text(new_content, encoding='utf-8')
            
            return f"파일이 업데이트되었습니다: {file_path}"
            
        except Exception as e:
            logger.error(f"노트 업데이트 실패: {str(e)}")
            return f"노트 업데이트 중 오류 발생: {str(e)}"
    
    def search_vault(
        self, 
        query: str, 
        file_pattern: str = "*.md", 
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        볼트 내 검색
        
        Args:
            query: 검색 쿼리
            file_pattern: 검색할 파일 패턴
            case_sensitive: 대소문자 구분 여부
        
        Returns:
            검색 결과 목록
        """
        try:
            results = []
            search_pattern = "**/" + file_pattern
            
            for file_path in self.vault_path.glob(search_pattern):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        
                        # 검색 쿼리 처리
                        search_text = content if case_sensitive else content.lower()
                        search_query = query if case_sensitive else query.lower()
                        
                        if search_query in search_text:
                            # 매칭된 라인 찾기
                            lines = content.split('\n')
                            matching_lines = []
                            
                            for i, line in enumerate(lines):
                                line_text = line if case_sensitive else line.lower()
                                if search_query in line_text:
                                    matching_lines.append({
                                        "line_number": i + 1,
                                        "content": line.strip()
                                    })
                            
                            results.append({
                                "file_path": str(file_path.relative_to(self.vault_path)),
                                "file_name": file_path.name,
                                "matches": len(matching_lines),
                                "matching_lines": matching_lines[:5]  # 최대 5개 라인만
                            })
                            
                    except Exception as e:
                        logger.warning(f"파일 검색 중 오류 ({file_path}): {str(e)}")
                        continue
            
            return sorted(results, key=lambda x: x["matches"], reverse=True)
            
        except Exception as e:
            logger.error(f"볼트 검색 실패: {str(e)}")
            return []
    
    def delete_file(self, file_path: str) -> str:
        """
        파일 삭제
        
        Args:
            file_path: 삭제할 파일 경로
        
        Returns:
            삭제 결과 메시지
        """
        try:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                return f"파일을 찾을 수 없습니다: {file_path}"
            
            full_path.unlink()
            return f"파일이 삭제되었습니다: {file_path}"
            
        except Exception as e:
            logger.error(f"파일 삭제 실패: {str(e)}")
            return f"파일 삭제 중 오류 발생: {str(e)}"
    
    def create_folder(self, folder_path: str) -> str:
        """
        폴더 생성
        
        Args:
            folder_path: 생성할 폴더 경로
        
        Returns:
            생성 결과 메시지
        """
        try:
            full_path = self.vault_path / folder_path
            full_path.mkdir(parents=True, exist_ok=True)
            
            return f"폴더가 생성되었습니다: {folder_path}"
            
        except Exception as e:
            logger.error(f"폴더 생성 실패: {str(e)}")
            return f"폴더 생성 중 오류 발생: {str(e)}"