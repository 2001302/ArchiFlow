#URS
## 프로젝트 개요

SW프로젝트의 효율적인 문서화와 시각화를 위한 프로그램입니다. 기본적으로 옵시디언 플러그인으로 개발합니다.

### 주요 제공 서비스
- AI를 활용한 소스코드 문서화 및 관리 시스템
- 문서화 포맷 설정
## 유저 플로우

### 네비게이션 구성
- 우측 편집 화면
	- 상단
	- 본문
		- 결과 답변창
	- 하단
		- 프롬프트 입력창
			- 상단
				- target document
				- 파일 첨부
				- 오른쪽 문서 형식
			- 중간
			- 하단
				- mode select
					- document
					- chat
				- medel select
- 매인 화면
### 상세 플로우
1. 문서화 포맷 설정
	- preset
	- custom
2. prompt only 또는 prompt+code 으로 문서 생성
3. code 또는 prompt+code으로 기존 문서 업데이트
	*target document가 없을땐 new document으로 동작 - MCP 필요*
	*target document가 태그되어 있다면 update document로 동작 - MCP 필요*
4. chat 모드
