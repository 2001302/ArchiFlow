ArchiFlow

# URS(User Requirement Specification)
## 프로젝트 개요
SW프로젝트의 효율적인 문서화와 시각화를 위한 프로그램입니다. 기본적으로 옵시디언 플러그인으로 개발합니다.
### 주요 제공 서비스
- SW설계 조언을 얻기 위한 채팅
- 소스코드를 다이어그램으로 시각화
- 프롬프트를 입력하여 다이어그램 생성
- prompt 입력으로 다이어그램 생성
- source 추가해서 다이어그램 생성
- 메인화면에서 편집화면으로 import 가능
- 편집화면에서 tool box 이용해서 편집 가능 
- 편집화면에서  마우스, 키보드를 이용해서 편집 가능

## 유저 플로우
### 네비게이션 구성
- 우측 편집 화면
    - 상단 버튼(다이어그램 선택,Tool Box,Setting)
    - 하단 모드 선택
        - Edit Mode
            - clear 버튼
            - 다이어그램 결과 창
                - 직접 편집 가능
                - 우클릭으로 prompt에 추가가능
            - prompt 입력 창
        - Chat Mode
            - clear 버튼
            - text 답변 창
            - prompt 입력 창
- 매인 화면
### 상세 플로우
1.Setting 창에서 사용할 AI API Key 설정
2.Create Mode에서 Prompt 입력하고 AI 답변을 받음
3.AI가 생성한 다이어그램을 적용할지 말지 결정
4.Edit Mode에서 메인화면에 존재하는 다이어그램 import
5.직접 편집하거나 Prompt를 입력해서 AI에 수정 요청
