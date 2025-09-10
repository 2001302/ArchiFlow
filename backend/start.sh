#!/bin/bash

# Obsidian AI Engine Backend 시작 스크립트

echo "🚀 Obsidian AI Engine Backend 시작 중..."

# 현재 디렉토리를 백엔드 폴더로 변경
cd "$(dirname "$0")"

# Python 가상환경 확인 및 생성
if [ ! -d "venv" ]; then
    echo "📦 Python 가상환경 생성 중..."
    python3 -m venv venv
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 의존성 설치
echo "📚 의존성 설치 중..."
pip install -r requirements.txt

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. env.example을 복사합니다..."
    cp env.example .env
    echo "📝 .env 파일을 편집하여 API 키를 설정해주세요."
fi

# 로그 디렉토리 생성
mkdir -p logs

# 서버 시작
echo "🌐 서버 시작 중..."
echo "📍 서버 주소: http://localhost:8000"
echo "📚 API 문서: http://localhost:8000/docs"
echo "=" * 50

python main.py
