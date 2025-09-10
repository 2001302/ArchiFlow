#!/usr/bin/env python3
"""
Backend Test Command
터미널에서 chat 모드로 대화할 수 있는 테스트 도구
"""
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.ai_engine import AIEngine, AIProvider, OutputFormat
from src.config import settings

class TestChat:
    """터미널 기반 채팅 테스트 도구"""
    
    def __init__(self):
        self.ai_engine = AIEngine()
        self.data_file = Path(__file__).parent.parent / "data.json"
        self.api_key = None
        self.provider = AIProvider.PERPLEXITY
        
    def load_api_key(self) -> bool:
        """data.json에서 API 키 로드"""
        try:
            if not self.data_file.exists():
                print("❌ data.json 파일을 찾을 수 없습니다.")
                print(f"   경로: {self.data_file}")
                return False
                
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 선택된 제공자에 따라 API 키 설정
            selected_provider = data.get('selectedProvider', 'perplexity')
            
            if selected_provider == 'perplexity':
                self.api_key = data.get('perplexityApiKey')
                self.provider = AIProvider.PERPLEXITY
            elif selected_provider == 'openai':
                self.api_key = data.get('openaiApiKey')
                self.provider = AIProvider.OPENAI
            elif selected_provider == 'anthropic':
                self.api_key = data.get('anthropicApiKey')
                self.provider = AIProvider.ANTHROPIC
            
            if not self.api_key:
                print(f"❌ {selected_provider} API 키가 설정되지 않았습니다.")
                print("   data.json 파일에서 API 키를 확인해주세요.")
                return False
                
            print(f"✅ {selected_provider.upper()} API 키를 로드했습니다.")
            return True
            
        except Exception as e:
            print(f"❌ API 키 로드 중 오류 발생: {e}")
            return False
    
    def print_welcome(self):
        """환영 메시지 출력"""
        print("=" * 60)
        print("🤖 AI Engine Test Chat")
        print("=" * 60)
        print(f"📡 제공자: {self.provider.value.upper()}")
        print("💡 명령어:")
        print("   /help     - 도움말 표시")
        print("   /format   - 출력 형식 변경")
        print("   /quit     - 종료")
        print("   /clear    - 화면 지우기")
        print("=" * 60)
        print()
    
    def print_help(self):
        """도움말 출력"""
        print("\n📚 사용 가능한 명령어:")
        print("   /help     - 이 도움말을 표시합니다")
        print("   /format   - 출력 형식 (text, mermaid, source_code)을 변경합니다")
        print("   /quit     - 채팅을 종료합니다")
        print("   /clear    - 화면을 지웁니다")
        print("   /status   - 현재 설정을 표시합니다")
        print("\n💬 일반 메시지는 AI에게 전송됩니다.")
        print()
    
    async def process_message(self, message: str, output_format: OutputFormat) -> str:
        """메시지 처리 및 AI 응답 생성"""
        try:
            result = await self.ai_engine.generate_response(
                prompt=message,
                output_format=output_format,
                provider=self.provider,
                api_key=self.api_key
            )
            
            if result.get('success'):
                return result.get('content', '응답이 비어있습니다.')
            else:
                return f"❌ 오류: {result.get('error', '알 수 없는 오류')}"
                
        except Exception as e:
            return f"❌ 처리 중 오류 발생: {str(e)}"
    
    async def run(self):
        """메인 채팅 루프 실행"""
        # API 키 로드
        if not self.load_api_key():
            return
        
        # 환영 메시지 출력
        self.print_welcome()
        
        # 현재 설정
        current_format = OutputFormat.TEXT
        
        while True:
            try:
                # 사용자 입력 받기
                user_input = input("👤 You: ").strip()
                
                # 빈 입력 처리
                if not user_input:
                    continue
                
                # 명령어 처리
                if user_input.startswith('/'):
                    command = user_input[1:].lower()
                    
                    if command == 'quit':
                        print("👋 채팅을 종료합니다. 안녕히 가세요!")
                        break
                    elif command == 'help':
                        self.print_help()
                        continue
                    elif command == 'clear':
                        print("\n" * 50)  # 화면 지우기
                        self.print_welcome()
                        continue
                    elif command == 'status':
                        print(f"\n📊 현재 설정:")
                        print(f"   제공자: {self.provider.value.upper()}")
                        print(f"   출력 형식: {current_format.value}")
                        print(f"   API 키: {'설정됨' if self.api_key else '설정되지 않음'}")
                        print()
                        continue
                    elif command == 'format':
                        print(f"\n📝 출력 형식 변경:")
                        print("   1. text (일반 텍스트)")
                        print("   2. mermaid (다이어그램)")
                        print("   3. source_code (소스 코드)")
                        
                        choice = input("선택 (1-3): ").strip()
                        if choice == '1':
                            current_format = OutputFormat.TEXT
                            print("✅ 출력 형식을 'text'로 변경했습니다.")
                        elif choice == '2':
                            current_format = OutputFormat.MERMAID
                            print("✅ 출력 형식을 'mermaid'로 변경했습니다.")
                        elif choice == '3':
                            current_format = OutputFormat.SOURCE_CODE
                            print("✅ 출력 형식을 'source_code'로 변경했습니다.")
                        else:
                            print("❌ 잘못된 선택입니다.")
                        print()
                        continue
                    else:
                        print(f"❌ 알 수 없는 명령어: {command}")
                        print("   /help를 입력하여 사용 가능한 명령어를 확인하세요.")
                        continue
                
                # AI 응답 생성
                print("🤖 AI가 응답을 생성하고 있습니다...")
                response = await self.process_message(user_input, current_format)
                
                # 응답 출력
                print(f"\n🤖 AI ({current_format.value}):")
                print("-" * 40)
                print(response)
                print("-" * 40)
                print()
                
            except KeyboardInterrupt:
                print("\n\n👋 채팅을 종료합니다. 안녕히 가세요!")
                break
            except Exception as e:
                print(f"\n❌ 오류 발생: {e}")
                print("계속하려면 Enter를 누르세요...")
                input()

def main():
    """메인 함수"""
    chat = TestChat()
    asyncio.run(chat.run())

if __name__ == "__main__":
    main()
