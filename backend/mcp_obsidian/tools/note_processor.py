"""
노트 처리기
노트 내용을 AI 결과와 결합하여 처리합니다.
"""
import re
from typing import Dict, Any, Optional
from loguru import logger


class NoteProcessor:
    """노트 처리기"""
    
    def __init__(self):
        self.obsidian_patterns = {
            "wikilink": r'\[\[([^\]]+)\]\]',
            "tag": r'#\w+',
            "heading": r'^#{1,6}\s+.+$',
            "code_block": r'```[\s\S]*?```',
            "inline_code": r'`[^`]+`'
        }
    
    def apply_ai_result(
        self, 
        original_content: str, 
        ai_result: str, 
        operation: str
    ) -> str:
        """
        AI 결과를 원본 노트에 적용
        
        Args:
            original_content: 원본 노트 내용
            ai_result: AI 처리 결과
            operation: 수행된 작업
        
        Returns:
            처리된 노트 내용
        """
        try:
            if operation == "summarize":
                return self._apply_summary(original_content, ai_result)
            elif operation == "enhance":
                return self._apply_enhancement(original_content, ai_result)
            elif operation == "generate_outline":
                return self._apply_outline(original_content, ai_result)
            elif operation == "translate":
                return self._apply_translation(original_content, ai_result)
            elif operation == "format":
                return self._apply_formatting(original_content, ai_result)
            else:
                return self._apply_general(original_content, ai_result, operation)
                
        except Exception as e:
            logger.error(f"AI 결과 적용 실패: {str(e)}")
            return original_content
    
    def _apply_summary(self, content: str, summary: str) -> str:
        """요약 결과 적용"""
        # 기존 요약 섹션이 있는지 확인
        summary_pattern = r'## 요약\s*\n.*?(?=\n##|\Z)'
        if re.search(summary_pattern, content, re.DOTALL):
            # 기존 요약 교체
            return re.sub(
                summary_pattern,
                f"## 요약\n\n{summary}\n",
                content,
                flags=re.DOTALL
            )
        else:
            # 새 요약 섹션 추가
            return f"{content}\n\n## 요약\n\n{summary}\n"
    
    def _apply_enhancement(self, content: str, enhancement: str) -> str:
        """개선 결과 적용"""
        # 기존 내용을 개선된 내용으로 교체
        return enhancement
    
    def _apply_outline(self, content: str, outline: str) -> str:
        """목차 결과 적용"""
        # 기존 목차 섹션이 있는지 확인
        outline_pattern = r'## 목차\s*\n.*?(?=\n##|\Z)'
        if re.search(outline_pattern, content, re.DOTALL):
            # 기존 목차 교체
            return re.sub(
                outline_pattern,
                f"## 목차\n\n{outline}\n",
                content,
                flags=re.DOTALL
            )
        else:
            # 새 목차 섹션 추가 (제목 다음에)
            lines = content.split('\n')
            insert_index = 0
            
            # 첫 번째 제목 찾기
            for i, line in enumerate(lines):
                if re.match(r'^#{1,6}\s+', line):
                    insert_index = i + 1
                    break
            
            lines.insert(insert_index, f"\n## 목차\n\n{outline}\n")
            return '\n'.join(lines)
    
    def _apply_translation(self, content: str, translation: str) -> str:
        """번역 결과 적용"""
        # 번역된 내용으로 완전 교체
        return translation
    
    def _apply_formatting(self, content: str, formatted: str) -> str:
        """포맷팅 결과 적용"""
        # 포맷팅된 내용으로 교체
        return formatted
    
    def _apply_general(self, content: str, result: str, operation: str) -> str:
        """일반적인 결과 적용"""
        # 작업별 섹션 추가
        section_title = f"## AI {operation.title()}\n\n"
        return f"{content}\n\n{section_title}{result}\n"
    
    def extract_metadata(self, content: str) -> Dict[str, Any]:
        """노트에서 메타데이터 추출"""
        metadata = {
            "title": self._extract_title(content),
            "tags": self._extract_tags(content),
            "links": self._extract_links(content),
            "headings": self._extract_headings(content),
            "word_count": len(content.split()),
            "char_count": len(content)
        }
        return metadata
    
    def _extract_title(self, content: str) -> Optional[str]:
        """제목 추출"""
        lines = content.split('\n')
        for line in lines:
            if re.match(r'^#\s+', line):
                return line[2:].strip()
        return None
    
    def _extract_tags(self, content: str) -> list:
        """태그 추출"""
        tags = re.findall(self.obsidian_patterns["tag"], content)
        return list(set(tags))  # 중복 제거
    
    def _extract_links(self, content: str) -> list:
        """링크 추출"""
        links = re.findall(self.obsidian_patterns["wikilink"], content)
        return list(set(links))  # 중복 제거
    
    def _extract_headings(self, content: str) -> list:
        """헤딩 추출"""
        headings = re.findall(self.obsidian_patterns["heading"], content, re.MULTILINE)
        return [h.strip() for h in headings]
    
    def validate_note_structure(self, content: str) -> Dict[str, Any]:
        """노트 구조 검증"""
        issues = []
        suggestions = []
        
        # 제목 확인
        if not self._extract_title(content):
            issues.append("제목이 없습니다.")
            suggestions.append("첫 번째 줄에 # 제목 형식으로 제목을 추가하세요.")
        
        # 헤딩 구조 확인
        headings = self._extract_headings(content)
        if len(headings) < 2:
            suggestions.append("더 많은 섹션을 추가하여 구조를 개선하세요.")
        
        # 태그 확인
        tags = self._extract_tags(content)
        if not tags:
            suggestions.append("관련 태그를 추가하여 노트를 분류하세요.")
        
        # 링크 확인
        links = self._extract_links(content)
        if not links:
            suggestions.append("다른 노트와의 연결을 위해 링크를 추가하세요.")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "suggestions": suggestions,
            "metadata": self.extract_metadata(content)
        }
    
    def format_note(self, content: str, style: str = "standard") -> str:
        """노트 포맷팅"""
        if style == "standard":
            return self._format_standard(content)
        elif style == "minimal":
            return self._format_minimal(content)
        elif style == "detailed":
            return self._format_detailed(content)
        else:
            return content
    
    def _format_standard(self, content: str) -> str:
        """표준 포맷팅"""
        lines = content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line:
                formatted_lines.append(line)
            else:
                formatted_lines.append('')
        
        # 연속된 빈 줄을 하나로 제한
        result = []
        prev_empty = False
        
        for line in formatted_lines:
            if line == '':
                if not prev_empty:
                    result.append('')
                prev_empty = True
            else:
                result.append(line)
                prev_empty = False
        
        return '\n'.join(result)
    
    def _format_minimal(self, content: str) -> str:
        """최소 포맷팅"""
        # 불필요한 공백 제거
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        return content.strip()
    
    def _format_detailed(self, content: str) -> str:
        """상세 포맷팅"""
        # 표준 포맷팅 적용
        content = self._format_standard(content)
        
        # 추가 구조화
        lines = content.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            if re.match(r'^#{1,6}\s+', line):
                # 헤딩 앞에 빈 줄 추가
                if i > 0 and lines[i-1] != '':
                    formatted_lines.append('')
                formatted_lines.append(line)
                # 헤딩 뒤에 빈 줄 추가
                if i < len(lines) - 1 and lines[i+1] != '':
                    formatted_lines.append('')
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
