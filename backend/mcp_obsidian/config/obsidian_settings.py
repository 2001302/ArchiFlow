"""
옵시디언 특화 설정
옵시디언 관련 설정을 관리합니다.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from loguru import logger


class ObsidianSettings:
    """옵시디언 특화 설정 클래스"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else None
        self.default_settings = {
            "vault_path": None,
            "default_note_format": "markdown",
            "auto_backup": True,
            "backup_interval": 3600,  # 초
            "max_note_size": 1024 * 1024,  # 1MB
            "supported_extensions": [".md", ".txt", ".json", ".yaml", ".yml"],
            "ai_enhancement": {
                "auto_summarize": False,
                "auto_tag": False,
                "auto_link": False,
                "suggest_improvements": True
            },
            "search_settings": {
                "case_sensitive": False,
                "use_regex": False,
                "include_metadata": True,
                "max_results": 50
            },
            "note_processing": {
                "auto_format": True,
                "validate_structure": True,
                "suggest_links": True,
                "extract_metadata": True
            },
            "vault_operations": {
                "create_backup_before_edit": True,
                "track_changes": True,
                "auto_save": True,
                "conflict_resolution": "prompt"  # prompt, auto, skip
            }
        }
        self.settings = self.default_settings.copy()
        self.load_settings()
    
    def load_settings(self) -> bool:
        """설정 파일에서 설정 로드"""
        if not self.config_path or not self.config_path.exists():
            return False
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
                self.settings.update(loaded_settings)
                return True
        except Exception as e:
            logger.error(f"설정 로드 실패: {str(e)}")
            return False
    
    def save_settings(self) -> bool:
        """설정을 파일에 저장"""
        if not self.config_path:
            return False
        
        try:
            # 디렉토리 생성
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
                return True
        except Exception as e:
            logger.error(f"설정 저장 실패: {str(e)}")
            return False
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """설정 값 조회"""
        keys = key.split('.')
        value = self.settings
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set_setting(self, key: str, value: Any) -> bool:
        """설정 값 설정"""
        try:
            keys = key.split('.')
            current = self.settings
            
            # 중첩된 딕셔너리 생성
            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]
            
            # 값 설정
            current[keys[-1]] = value
            return True
        except Exception as e:
            logger.error(f"설정 설정 실패: {str(e)}")
            return False
    
    def get_vault_path(self) -> Optional[str]:
        """볼트 경로 조회"""
        return self.get_setting("vault_path")
    
    def set_vault_path(self, vault_path: str) -> bool:
        """볼트 경로 설정"""
        path = Path(vault_path)
        if not path.exists():
            logger.error(f"볼트 경로가 존재하지 않습니다: {vault_path}")
            return False
        
        return self.set_setting("vault_path", str(path.absolute()))
    
    def get_ai_enhancement_settings(self) -> Dict[str, Any]:
        """AI 향상 설정 조회"""
        return self.get_setting("ai_enhancement", {})
    
    def set_ai_enhancement_setting(self, key: str, value: Any) -> bool:
        """AI 향상 설정 변경"""
        return self.set_setting(f"ai_enhancement.{key}", value)
    
    def get_search_settings(self) -> Dict[str, Any]:
        """검색 설정 조회"""
        return self.get_setting("search_settings", {})
    
    def set_search_setting(self, key: str, value: Any) -> bool:
        """검색 설정 변경"""
        return self.set_setting(f"search_settings.{key}", value)
    
    def get_note_processing_settings(self) -> Dict[str, Any]:
        """노트 처리 설정 조회"""
        return self.get_setting("note_processing", {})
    
    def set_note_processing_setting(self, key: str, value: Any) -> bool:
        """노트 처리 설정 변경"""
        return self.set_setting(f"note_processing.{key}", value)
    
    def get_vault_operations_settings(self) -> Dict[str, Any]:
        """볼트 작업 설정 조회"""
        return self.get_setting("vault_operations", {})
    
    def set_vault_operations_setting(self, key: str, value: Any) -> bool:
        """볼트 작업 설정 변경"""
        return self.set_setting(f"vault_operations.{key}", value)
    
    def validate_settings(self) -> Dict[str, Any]:
        """설정 유효성 검사"""
        issues = []
        warnings = []
        
        # 볼트 경로 검사
        vault_path = self.get_vault_path()
        if not vault_path:
            issues.append("볼트 경로가 설정되지 않았습니다.")
        elif not Path(vault_path).exists():
            issues.append(f"볼트 경로가 존재하지 않습니다: {vault_path}")
        
        # 지원 확장자 검사
        extensions = self.get_setting("supported_extensions", [])
        if not extensions:
            warnings.append("지원 확장자가 설정되지 않았습니다.")
        
        # AI 향상 설정 검사
        ai_settings = self.get_ai_enhancement_settings()
        if not isinstance(ai_settings, dict):
            issues.append("AI 향상 설정이 올바르지 않습니다.")
        
        # 검색 설정 검사
        search_settings = self.get_search_settings()
        max_results = search_settings.get("max_results", 50)
        if not isinstance(max_results, int) or max_results <= 0:
            warnings.append("최대 검색 결과 수가 올바르지 않습니다.")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    def reset_to_defaults(self) -> bool:
        """설정을 기본값으로 재설정"""
        try:
            self.settings = self.default_settings.copy()
            return True
        except Exception as e:
            logger.error(f"설정 재설정 실패: {str(e)}")
            return False
    
    def export_settings(self, export_path: str) -> bool:
        """설정을 파일로 내보내기"""
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
                return True
        except Exception as e:
            logger.error(f"설정 내보내기 실패: {str(e)}")
            return False
    
    def import_settings(self, import_path: str) -> bool:
        """설정 파일에서 가져오기"""
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                logger.error(f"설정 파일이 존재하지 않습니다: {import_path}")
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
                self.settings.update(imported_settings)
                return True
        except Exception as e:
            logger.error(f"설정 가져오기 실패: {str(e)}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """모든 설정 조회"""
        return self.settings.copy()
    
    def update_settings(self, new_settings: Dict[str, Any]) -> bool:
        """설정 일괄 업데이트"""
        try:
            self.settings.update(new_settings)
            return True
        except Exception as e:
            logger.error(f"설정 업데이트 실패: {str(e)}")
            return False
