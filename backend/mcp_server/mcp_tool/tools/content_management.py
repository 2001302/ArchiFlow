"""
콘텐츠 관리 도구들
메타데이터 추출, 태그 관리, 콘텐츠 정리 등
"""
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger

class ContentManagementTools:
    """콘텐츠 관리 도구 클래스"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        파일에서 메타데이터 추출
        
        Args:
            file_path: 메타데이터를 추출할 파일 경로
        
        Returns:
            추출된 메타데이터
        """
        try:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                return {"error": f"파일을 찾을 수 없습니다: {file_path}"}
            
            content = full_path.read_text(encoding='utf-8')
            
            metadata = {
                "file_path": file_path,
                "file_name": full_path.name,
                "file_size": full_path.stat().st_size,
                "tags": self._extract_tags(content),
                "headings": self._extract_headings(content),
                "links": self._extract_links(content),
                "word_count": len(content.split()),
                "line_count": len(content.split('\n')),
                "has_frontmatter": self._has_frontmatter(content)
            }
            
            # 프론트매터가 있는 경우 추출
            if metadata["has_frontmatter"]:
                metadata["frontmatter"] = self._extract_frontmatter(content)
            
            return metadata
            
        except Exception as e:
            logger.error(f"메타데이터 추출 실패: {str(e)}")
            return {"error": f"메타데이터 추출 중 오류 발생: {str(e)}"}
    
    def _extract_tags(self, content: str) -> List[str]:
        """태그 추출"""
        # Obsidian 태그 패턴: #tag 또는 #tag/subtag
        tag_pattern = r'#([a-zA-Z0-9가-힣_-]+(?:\/[a-zA-Z0-9가-힣_-]+)*)'
        tags = re.findall(tag_pattern, content)
        return list(set(tags))  # 중복 제거
    
    def _extract_headings(self, content: str) -> List[Dict[str, Any]]:
        """헤딩 추출"""
        headings = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # Markdown 헤딩 패턴: # ## ### 등
            match = re.match(r'^(#{1,6})\s+(.+)', line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    "level": level,
                    "text": text,
                    "line_number": i + 1
                })
        
        return headings
    
    def _extract_links(self, content: str) -> List[Dict[str, str]]:
        """링크 추출"""
        links = []
        
        # Markdown 링크 패턴: [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, url in markdown_links:
            links.append({
                "type": "markdown",
                "text": text,
                "url": url
            })
        
        # Obsidian 내부 링크 패턴: [[link]] 또는 [[link|display]]
        obsidian_links = re.findall(r'\[\[([^|\]]+)(?:\|([^\]]+))?\]\]', content)
        for link, display in obsidian_links:
            links.append({
                "type": "obsidian",
                "link": link,
                "display": display or link
            })
        
        return links
    
    def _has_frontmatter(self, content: str) -> bool:
        """프론트매터 존재 여부 확인"""
        return content.startswith('---\n')
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """프론트매터 추출"""
        try:
            if not self._has_frontmatter(content):
                return {}
            
            lines = content.split('\n')
            frontmatter_lines = []
            
            for i, line in enumerate(lines[1:], 1):  # 첫 번째 --- 건너뛰기
                if line.strip() == '---':
                    break
                frontmatter_lines.append(line)
            
            frontmatter_text = '\n'.join(frontmatter_lines)
            
            # YAML 파싱 시도
            try:
                import yaml
                return yaml.safe_load(frontmatter_text) or {}
            except ImportError:
                # YAML이 없는 경우 간단한 파싱
                return self._parse_simple_yaml(frontmatter_text)
                
        except Exception as e:
            logger.warning(f"프론트매터 파싱 실패: {str(e)}")
            return {}
    
    def _parse_simple_yaml(self, text: str) -> Dict[str, Any]:
        """간단한 YAML 파싱"""
        result = {}
        for line in text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # 값 타입 변환
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                elif value.isdigit():
                    value = int(value)
                
                result[key] = value
        
        return result
    
    def manage_tags(
        self, 
        file_path: str, 
        action: str, 
        tags: List[str] = None
    ) -> str:
        """
        태그 관리
        
        Args:
            file_path: 태그를 관리할 파일 경로
            action: 태그 작업 (add, remove, list)
            tags: 태그 목록
        
        Returns:
            작업 결과 메시지
        """
        try:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                return f"파일을 찾을 수 없습니다: {file_path}"
            
            content = full_path.read_text(encoding='utf-8')
            current_tags = self._extract_tags(content)
            
            if action == "list":
                return f"현재 태그: {', '.join(current_tags)}"
            
            if action == "add" and tags:
                # 새 태그 추가
                new_tags = [tag for tag in tags if tag not in current_tags]
                if new_tags:
                    tag_line = " ".join([f"#{tag}" for tag in new_tags])
                    if content.strip():
                        content = f"{tag_line}\n\n{content}"
                    else:
                        content = tag_line
                    
                    full_path.write_text(content, encoding='utf-8')
                    return f"태그가 추가되었습니다: {', '.join(new_tags)}"
                else:
                    return "추가할 새 태그가 없습니다."
            
            elif action == "remove" and tags:
                # 태그 제거
                removed_tags = []
                for tag in tags:
                    if tag in current_tags:
                        # 태그 제거
                        content = re.sub(rf'#{re.escape(tag)}\b', '', content)
                        removed_tags.append(tag)
                
                if removed_tags:
                    # 빈 줄 정리
                    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
                    full_path.write_text(content, encoding='utf-8')
                    return f"태그가 제거되었습니다: {', '.join(removed_tags)}"
                else:
                    return "제거할 태그가 없습니다."
            
            else:
                return "잘못된 작업 또는 태그가 지정되지 않았습니다."
                
        except Exception as e:
            logger.error(f"태그 관리 실패: {str(e)}")
            return f"태그 관리 중 오류 발생: {str(e)}"
    
    def organize_content(
        self, 
        file_path: str, 
        strategy: str
    ) -> str:
        """
        콘텐츠 정리 및 분류
        
        Args:
            file_path: 정리할 파일 경로
            strategy: 정리 전략
        
        Returns:
            정리 결과 메시지
        """
        try:
            full_path = self.vault_path / file_path
            if not full_path.exists():
                return f"파일을 찾을 수 없습니다: {file_path}"
            
            content = full_path.read_text(encoding='utf-8')
            
            if strategy == "auto_categorize":
                return self._auto_categorize(content, full_path)
            elif strategy == "add_structure":
                return self._add_structure(content, full_path)
            elif strategy == "extract_keywords":
                return self._extract_keywords(content, full_path)
            else:
                return f"지원하지 않는 정리 전략: {strategy}"
                
        except Exception as e:
            logger.error(f"콘텐츠 정리 실패: {str(e)}")
            return f"콘텐츠 정리 중 오류 발생: {str(e)}"
    
    def _auto_categorize(self, content: str, file_path: Path) -> str:
        """자동 카테고리 분류"""
        # 간단한 키워드 기반 분류
        categories = {
            "개발": ["코드", "프로그래밍", "개발", "API", "함수", "클래스"],
            "문서": ["문서", "가이드", "설명", "튜토리얼", "매뉴얼"],
            "아이디어": ["아이디어", "생각", "계획", "제안", "개선"],
            "회의": ["회의", "미팅", "논의", "토론", "결정"],
            "학습": ["학습", "공부", "연구", "조사", "분석"]
        }
        
        content_lower = content.lower()
        matched_categories = []
        
        for category, keywords in categories.items():
            if any(keyword in content_lower for keyword in keywords):
                matched_categories.append(category)
        
        if matched_categories:
            # 카테고리 태그 추가
            category_tags = " ".join([f"#{cat}" for cat in matched_categories])
            if not content.startswith('#'):
                content = f"{category_tags}\n\n{content}"
            else:
                # 기존 태그에 추가
                lines = content.split('\n')
                if lines[0].startswith('#'):
                    lines[0] = f"{lines[0]} {category_tags}"
                    content = '\n'.join(lines)
            
            file_path.write_text(content, encoding='utf-8')
            return f"자동 분류 완료: {', '.join(matched_categories)}"
        else:
            return "분류할 수 있는 카테고리를 찾지 못했습니다."
    
    def _add_structure(self, content: str, file_path: Path) -> str:
        """구조 추가"""
        lines = content.split('\n')
        structured_lines = []
        
        # 제목이 없으면 첫 번째 줄을 제목으로
        if not any(line.strip().startswith('#') for line in lines[:3]):
            if lines[0].strip():
                structured_lines.append(f"# {lines[0].strip()}")
                structured_lines.append("")
                structured_lines.extend(lines[1:])
            else:
                structured_lines = lines
        else:
            structured_lines = lines
        
        # 빈 줄 정리
        cleaned_lines = []
        prev_empty = False
        for line in structured_lines:
            if line.strip() == "":
                if not prev_empty:
                    cleaned_lines.append(line)
                prev_empty = True
            else:
                cleaned_lines.append(line)
                prev_empty = False
        
        file_path.write_text('\n'.join(cleaned_lines), encoding='utf-8')
        return "구조가 추가되었습니다."
    
    def _extract_keywords(self, content: str, file_path: Path) -> str:
        """키워드 추출"""
        # 간단한 키워드 추출 (한글, 영문 단어)
        words = re.findall(r'[가-힣a-zA-Z]+', content)
        
        # 빈도 계산
        word_count = {}
        for word in words:
            if len(word) > 1:  # 1글자 단어 제외
                word_count[word] = word_count.get(word, 0) + 1
        
        # 상위 키워드 선택
        top_keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # 키워드 태그로 추가
        keyword_tags = " ".join([f"#{word}" for word, count in top_keywords])
        
        if not content.startswith('#'):
            content = f"{keyword_tags}\n\n{content}"
        else:
            lines = content.split('\n')
            if lines[0].startswith('#'):
                lines[0] = f"{lines[0]} {keyword_tags}"
                content = '\n'.join(lines)
        
        file_path.write_text(content, encoding='utf-8')
        return f"키워드가 추출되었습니다: {', '.join([word for word, count in top_keywords])}"