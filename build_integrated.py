#!/usr/bin/env python3
"""
통합된 백엔드 실행파일 빌드 스크립트
PyInstaller를 사용하여 통합된 백엔드(API + AI Core)를 실행파일로 빌드합니다.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    # 프로젝트 루트 디렉토리
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"
    logs_dir = project_root / "logs"
    
    print("🚀 통합 백엔드 실행파일 빌드 시작...")
    print(f"📁 프로젝트 루트: {project_root}")
    print(f"📁 Backend 디렉토리: {backend_dir}")
    print("🔗 통합 기능: REST API + AI Core")
    
    # 기존 빌드 파일들 정리
    if dist_dir.exists():
        print("🧹 기존 dist 디렉토리 정리 중...")
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        print("🧹 기존 build 디렉토리 정리 중...")
        shutil.rmtree(build_dir)
    
    if logs_dir.exists():
        print("🧹 기존 logs 디렉토리 정리 중...")
        shutil.rmtree(logs_dir)
    
    # PyInstaller 명령어 구성
    main_script = backend_dir / "main.py"
    
    # 가상환경의 pyinstaller 경로 사용
    venv_pyinstaller = backend_dir / "venv" / "bin" / "pyinstaller"
    if not venv_pyinstaller.exists():
        print("❌ 가상환경에서 pyinstaller를 찾을 수 없습니다.")
        return False
    
    pyinstaller_cmd = [
        str(venv_pyinstaller),
        "--onefile",  # 단일 실행파일로 생성
        "--name", "documize-integrated",  # 실행파일 이름
        "--distpath", str(dist_dir),  # 출력 디렉토리
        "--workpath", str(build_dir),  # 임시 빌드 디렉토리
        "--specpath", str(project_root),  # spec 파일 위치
        "--add-data", f"{backend_dir / 'mcp_server'}{os.pathsep}mcp_server",  # mcp_server 디렉토리 포함
        "--add-data", f"{backend_dir / 'documize_api'}{os.pathsep}documize_api",  # documize_api 디렉토리 포함
        # FastAPI 관련 의존성
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.loops.asyncio",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.http.h11_impl",
        "--hidden-import", "uvicorn.protocols.http.httptools_impl",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "fastapi",
        "--hidden-import", "pydantic",
        "--hidden-import", "pydantic_settings",
        # AI 제공자 관련 의존성
        "--hidden-import", "openai",
        "--hidden-import", "anthropic",
        "--hidden-import", "httpx",
        "--hidden-import", "loguru",
        "--hidden-import", "jinja2",
        "--hidden-import", "python_multipart",
        # AI Core 모듈들
        "--hidden-import", "mcp_server",
        "--hidden-import", "mcp_server.providers",
        "--hidden-import", "mcp_server.managers",
        "--hidden-import", "mcp_server.models",
        "--hidden-import", "mcp_server.utils",
        "--hidden-import", "mcp_server.config",
        "--hidden-import", "mcp_server.processors",
        "--hidden-import", "mcp_server.mcp_tool",
        "--hidden-import", "mcp_server.mcp_tool.tools",
        "--hidden-import", "mcp_server.mcp_tool.tools.ai_generation",
        "--hidden-import", "mcp_server.mcp_tool.tools.vault_operations",
        "--hidden-import", "mcp_server.mcp_tool.tools.content_management",
        # Documize API 모듈들
        "--hidden-import", "documize_api",
        "--hidden-import", "documize_api.main",
        str(main_script)
    ]
    
    print("🔨 PyInstaller 실행 중...")
    print(f"명령어: {' '.join(pyinstaller_cmd)}")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(pyinstaller_cmd, cwd=project_root, check=True, capture_output=True, text=True)
        print("✅ 빌드 성공!")
        
        # 실행파일 경로 확인
        executable_path = dist_dir / "documize-integrated"
        if sys.platform == "win32":
            executable_path = dist_dir / "documize-integrated.exe"
        
        if executable_path.exists():
            print(f"📦 실행파일 생성됨: {executable_path}")
            print(f"📏 파일 크기: {executable_path.stat().st_size / 1024 / 1024:.2f} MB")
            
            # 사용법 안내
            print("\n🎉 통합 백엔드 빌드 완료!")
            print("=" * 50)
            print("📋 사용법:")
            print(f"  실행: {executable_path}")
            print("  서버 주소: http://localhost:8000")
            print("  API 문서: http://localhost:8000/docs")
            print("\n🔗 주요 엔드포인트:")
            print("  - POST /generate - AI 응답 생성")
            print("  - GET /vault/files - 볼트 파일 목록")
            print("  - POST /vault/notes - 노트 생성")
            print("  - GET /vault/search - 볼트 검색")
            print("=" * 50)
        else:
            print("❌ 실행파일이 생성되지 않았습니다.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"에러 출력: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
