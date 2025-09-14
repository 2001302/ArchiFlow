#!/usr/bin/env python3
"""
테스트 실행 스크립트
"""
import subprocess
import sys
import os
from pathlib import Path

def run_tests():
    """테스트 실행"""
    print("🧪 AI 엔진 백엔드 테스트 실행")
    print("=" * 50)
    
    # 현재 디렉토리를 백엔드 디렉토리로 설정
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        # 기본 테스트 실행
        print("📋 기본 테스트 실행 중...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 모든 테스트가 성공적으로 통과했습니다!")
        else:
            print("❌ 일부 테스트가 실패했습니다.")
            print(result.stdout)
            print(result.stderr)
            return False
        
        # 커버리지 테스트 실행
        print("\n📊 테스트 커버리지 분석 중...")
        coverage_result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", 
            "--cov=ai_core", "--cov=documize_api", 
            "--cov-report=term", "--cov-report=html"
        ], capture_output=True, text=True)
        
        if coverage_result.returncode == 0:
            print("✅ 커버리지 분석이 완료되었습니다!")
            print(f"📁 HTML 커버리지 보고서: {backend_dir}/htmlcov/index.html")
        else:
            print("⚠️ 커버리지 분석 중 일부 문제가 발생했습니다.")
            print(coverage_result.stdout)
            print(coverage_result.stderr)
        
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        return False

def run_specific_test(test_name):
    """특정 테스트 실행"""
    print(f"🎯 특정 테스트 실행: {test_name}")
    print("=" * 50)
    
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", f"tests/{test_name}", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        return False

def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        # 특정 테스트 실행
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # 모든 테스트 실행
        success = run_tests()
    
    if success:
        print("\n🎉 테스트 실행이 완료되었습니다!")
        sys.exit(0)
    else:
        print("\n💥 테스트 실행에 실패했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()
