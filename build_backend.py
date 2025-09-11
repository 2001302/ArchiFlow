#!/usr/bin/env python3
"""
Backend 실행파일 빌드 스크립트
PyInstaller를 사용하여 backend를 실행파일로 빌드합니다.
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
    
    print("🚀 Backend 실행파일 빌드 시작...")
    print(f"📁 프로젝트 루트: {project_root}")
    print(f"📁 Backend 디렉토리: {backend_dir}")
    
    # 기존 빌드 파일들 정리
    if dist_dir.exists():
        print("🧹 기존 dist 디렉토리 정리 중...")
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        print("🧹 기존 build 디렉토리 정리 중...")
        shutil.rmtree(build_dir)
    
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
        "--name", "arch-flow-backend",  # 실행파일 이름
        "--distpath", str(dist_dir),  # 출력 디렉토리
        "--workpath", str(build_dir),  # 임시 빌드 디렉토리
        "--specpath", str(project_root),  # spec 파일 위치
        "--add-data", f"{backend_dir / 'src'}{os.pathsep}src",  # src 디렉토리 포함
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.loops.asyncio",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.http.h11_impl",
        "--hidden-import", "uvicorn.protocols.http.httptools_impl",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "fastapi",
        "--hidden-import", "pydantic",
        "--hidden-import", "openai",
        "--hidden-import", "anthropic",
        "--hidden-import", "httpx",
        "--hidden-import", "loguru",
        "--hidden-import", "jinja2",
        "--hidden-import", "python_multipart",
        str(main_script)
    ]
    
    print("🔨 PyInstaller 실행 중...")
    print(f"명령어: {' '.join(pyinstaller_cmd)}")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(pyinstaller_cmd, cwd=project_root, check=True, capture_output=True, text=True)
        print("✅ 빌드 성공!")
        
        # 실행파일 경로 확인
        executable_path = dist_dir / "arch-flow-backend"
        if sys.platform == "win32":
            executable_path = dist_dir / "arch-flow-backend.exe"
        
        if executable_path.exists():
            print(f"📦 실행파일 생성됨: {executable_path}")
            print(f"📏 파일 크기: {executable_path.stat().st_size / 1024 / 1024:.2f} MB")
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
    
    print("\n🎉 빌드 완료!")
    print(f"실행파일 위치: {executable_path}")
    print("이제 frontend에서 이 실행파일을 실행할 수 있습니다.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
