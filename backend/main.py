#!/usr/bin/env python3
"""
AI 엔진 백엔드 메인 실행 파일
"""
import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_server import run_server

if __name__ == "__main__":
    print("🚀 Obsidian AI Engine Backend 시작 중...")
    print(f"📁 프로젝트 루트: {project_root}")
    print("🌐 서버가 시작되면 http://localhost:8000 에서 확인할 수 있습니다")
    print("📚 API 문서는 http://localhost:8000/docs 에서 확인할 수 있습니다")
    print("=" * 50)
    
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n👋 서버가 종료되었습니다.")
    except Exception as e:
        print(f"❌ 서버 실행 중 오류 발생: {e}")
        sys.exit(1)
