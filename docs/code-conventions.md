## 코드 컨벤션 (Obsidian Sample Plugin)

### 파일/폴더 구조
- **src 분리**: 런타임 클래스/유틸은 `src/` 폴더에 위치합니다.
- **파일명 대소문자**:
  - 공개 상수/타입 파일은 PascalCase 사용: `Constants.ts`, `Settings.ts` (리눅스 CI에서 케이스 민감 문제 방지).
  - 클래스 파일도 PascalCase: `SidePannelView.ts`, `SampleModal.ts`, `SampleSettingTab.ts`.
  - 루트 엔트리: `main.ts` (Obsidian 빌드/번들 타겟).

### 임포트 규칙
- **정렬 순서**: 외부 라이브러리 → 내부 경로 → 상대 경로 깊은 순서.
- **경로 케이스 일치**: 실제 파일명과 정확히 같은 케이스로 임포트합니다.
  - 예: `import { VIEW_TYPE_ARCHIFLOW } from './src/Constants';`
- **엔트리 분리**: `main.ts`는 플러그인 수명주기만 담당하고, 뷰/모달/설정 탭은 `src/`에서 임포트합니다.

### 명명 규칙
- **클래스/타입**: PascalCase (예: `MyPlugin`, `SidePannelView`, `MyPluginSettings`).
- **상수**: UPPER_SNAKE_CASE (예: `VIEW_TYPE_ARCHIFLOW`).
- **변수/함수**: camelCase (예: `activateRightPanel`).
- **파일명**: 클래스/상수/설정 등 공개 개념은 PascalCase 파일명 사용.

### 코드 스타일
- **탭 들여쓰기**: 기존 코드와 동일하게 탭 사용. 혼용 금지.
- **세미콜론**: 사용하지 않음(현재 코드 스타일 준수).
- **문자열**: 작은따옴표 `'` 기본.
- **가독성**: 한 줄이 길어지면 줄바꿈. 중첩은 2~3단계 이내 유지.

### TypeScript 설정/타입
- `strictNullChecks: true`, `noImplicitAny: true`를 전제로 안전한 타입 작성.
- 공개 API(클래스 메서드) 반환 타입 명시.
- 불필요한 `any` 사용 금지.

### Obsidian 플러그인 구조
- `Plugin`과 `ItemView`는 **역할 분리**:
  - `main.ts` → `Plugin` 수명주기, 명령/리본/세팅 탭/뷰 등록.
  - `src/SidePannelView.ts` → `ItemView` UI/상태.
  - `src/SampleModal.ts`, `src/SampleSettingTab.ts` → 각자 책임 분리.
- 뷰 타입 상수는 `src/Constants.ts`에 정의하고 재사용.

### 설정 관리
- 설정 타입/기본값은 `src/Settings.ts` 에 위치:
  - `export interface MyPluginSettings { ... }`
  - `export const DEFAULT_SETTINGS: MyPluginSettings = { ... }`

### 커밋/버전
- 릴리즈 태그 접두사는 `.npmrc`에 따라 빈 문자열(예: `1.2.3`).
- 버전 변경은 `npm run version` 스크립트를 사용해 `manifest.json`, `versions.json` 동기화.

### 품질 규칙
- 빌드 전 `tsc -noEmit -skipLibCheck` 통과 필수 (`npm run build` 포함).
- 파일 케이스 불일치 방지를 위해 `tsconfig.json`에 다음 옵션 사용 권장:
  ```json
  {
    "compilerOptions": {
      "forceConsistentCasingInFileNames": true
    }
  }
  ```


