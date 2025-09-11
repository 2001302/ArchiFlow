#!/usr/bin/env python3
"""
전체 프로젝트 빌드 스크립트
프론트엔드(npm run build)와 백엔드(build_backend.py)를 순차적으로 빌드합니다.
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, description=""):
    """명령어를 실행하고 결과를 반환합니다."""
    print(f"🔨 {description}")
    print(f"명령어: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=True, 
            capture_output=True, 
            text=True,
            shell=True if isinstance(cmd, str) else False
        )
        print(f"✅ {description} 완료!")
        if result.stdout:
            print(f"출력: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패: {e}")
        if e.stderr:
            print(f"에러 출력: {e.stderr}")
        if e.stdout:
            print(f"표준 출력: {e.stdout}")
        return False
    except Exception as e:
        print(f"❌ {description} 중 예상치 못한 오류: {e}")
        return False

def check_dependencies():
    """필요한 의존성이 설치되어 있는지 확인합니다."""
    print("🔍 의존성 확인 중...")
    
    # Node.js 확인
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js 버전: {result.stdout.strip()}")
        else:
            print("❌ Node.js가 설치되어 있지 않습니다.")
            return False
    except FileNotFoundError:
        print("❌ Node.js가 설치되어 있지 않습니다.")
        return False
    
    # npm 확인
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm 버전: {result.stdout.strip()}")
        else:
            print("❌ npm이 설치되어 있지 않습니다.")
            return False
    except FileNotFoundError:
        print("❌ npm이 설치되어 있지 않습니다.")
        return False
    
    # Python 확인
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python3 버전: {result.stdout.strip()}")
        else:
            print("❌ Python3가 설치되어 있지 않습니다.")
            return False
    except FileNotFoundError:
        print("❌ Python3가 설치되어 있지 않습니다.")
        return False
    
    return True

def build_frontend(project_root):
    """프론트엔드를 빌드합니다."""
    frontend_dir = project_root / "frontend"
    
    if not frontend_dir.exists():
        print("❌ frontend 디렉토리를 찾을 수 없습니다.")
        return False
    
    print("\n" + "="*50)
    print("🎨 프론트엔드 빌드 시작")
    print("="*50)
    
    # npm install 실행 (의존성 설치)
    if not run_command("npm install", cwd=frontend_dir, description="npm 의존성 설치"):
        return False
    
    # npm run build 실행
    if not run_command("npm run build", cwd=frontend_dir, description="프론트엔드 빌드"):
        return False
    
    return True

def build_backend(project_root):
    """백엔드를 빌드합니다."""
    print("\n" + "="*50)
    print("⚙️ 백엔드 빌드 시작")
    print("="*50)
    
    # build_backend.py 실행
    build_script = project_root / "build_backend.py"
    if not build_script.exists():
        print("❌ build_backend.py 파일을 찾을 수 없습니다.")
        return False
    
    if not run_command(["python3", str(build_script)], cwd=project_root, description="백엔드 빌드"):
        return False
    
    return True

def main():
    """메인 빌드 프로세스를 실행합니다."""
    # 프로젝트 루트 디렉토리
    project_root = Path(__file__).parent
    
    print("🚀 전체 프로젝트 빌드 시작...")
    print(f"📁 프로젝트 루트: {project_root}")
    
    # 의존성 확인
    if not check_dependencies():
        print("❌ 필요한 의존성이 설치되어 있지 않습니다.")
        return False
    
    # 프론트엔드 빌드
    if not build_frontend(project_root):
        print("❌ 프론트엔드 빌드에 실패했습니다.")
        return False
    
    # 백엔드 빌드
    if not build_backend(project_root):
        print("❌ 백엔드 빌드에 실패했습니다.")
        return False
    
    print("\n" + "="*50)
    print("🎉 전체 빌드 완료!")
    print("="*50)
    print("✅ 프론트엔드와 백엔드가 모두 성공적으로 빌드되었습니다.")
    print(f"📦 빌드된 파일들:")
    print(f"   - 프론트엔드: {project_root / 'main.js'}")
    print(f"   - 백엔드: {project_root / 'dist' / 'arch-flow-backend'}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
