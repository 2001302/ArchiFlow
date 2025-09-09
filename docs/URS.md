ArchiFlow

# URS(User Requirement Specification)
## 프로젝트 개요
SW프로젝트의 효율적인 문서화와 시각화를 위한 프로그램입니다. 기본적으로 옵시디언 플러그인으로 개발합니다.
### 주요 제공 서비스
- 채팅
- 소스코드를 다이어그램으로 시각화
- 프롬프트를 입력하여 다이어그램 생성
- 구조 안정성 평가
- 다이어그램으로 소스코드 생성

## 유저 플로우
### 네비게이션 구성
- 우측 편집 화면
    - 상단 버튼(모드 선택,Tool Box,Setting)
    - 모드 선택
        - Diagram Mode
            - 다이어그램 결과 창
                - 더보기 버튼
                    - Edit
                    - Apply
            - prompt 입력 창
                - 다이어그램 타입
                - 메인화면 다이어그램 태그
                - 소스파일 태그
        - Chat Mode
            - text 답변 창
            - prompt 입력 창
        - Source Mode
            - 소스코드 답변 창
            - prompt 입력 창
                - 메인화면 다이어그램 태그
- 매인 화면
    - ArchFlow 전용 

### 상세 플로우
1.Diagram Mode(결과물을 Diagram으로 받음)
    Create Diagram
        - prompt 입력,source 태그해서 답변을 받음
        - insert 하면서 arch-flow 코드블럭으로 변환
    Edit Diagram
        - arch-flow 코드블럭 태그
        - source 태그
        - 프롬프트 입력
        위 동작으로 답변을 받음
2.Source Mode(결과물을 Source으로 받음)
    Create Source
        - arch-flow 코드블럭 태그
        - source 태그
        - 프롬프트 입력
        위 동작으로 답변을 받음
2.Chat Mode
    - 일반적인 채팅 기능
