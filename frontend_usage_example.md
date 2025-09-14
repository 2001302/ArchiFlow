# Frontend AI 요청 사용 가이드

## 개요
이제 backend에서 모든 AI 요청을 MCP 서버를 통해서만 처리하도록 리팩토링되었습니다. Frontend에서는 요청 유형에 따라 적절한 엔드포인트를 선택할 수 있습니다.

## API 엔드포인트

### 1. 기본 AI 요청 (`/ai/basic/generate`)
**용도**: 간단한 질문/답변, 일반적인 텍스트 생성
```typescript
// 기본 AI 요청 예제
const basicAIRequest = async (prompt: string) => {
  const response = await fetch('http://localhost:8000/ai/basic/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: prompt,
      provider: 'perplexity',
      model: 'gpt-4',
      api_key: 'your-api-key'
    })
  });
  return await response.json();
};

// 사용 예제
const result = await basicAIRequest("파이썬에서 리스트를 정렬하는 방법을 알려주세요");
console.log(result.content); // AI 응답 텍스트
```

### 2. 고급 AI 요청 (`/ai/advanced/generate`)
**용도**: 코드 생성, 구조화된 문서 작성
```typescript
// 고급 AI 요청 예제
const advancedAIRequest = async (prompt: string, language: string = 'python') => {
  const response = await fetch('http://localhost:8000/ai/advanced/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt: prompt,
      provider: 'perplexity',
      model: 'gpt-4',
      api_key: 'your-api-key',
      language: language
    })
  });
  return await response.json();
};

// 사용 예제
const result = await advancedAIRequest(
  "사용자 인증 시스템을 만들어주세요", 
  "python"
);
console.log(result.content); // 구조화된 코드/문서
```

### 3. MCP 도구 직접 호출 (`/mcp/tools/call`)
**용도**: 볼트 파일 조작, 검색, 메타데이터 관리
```typescript
// MCP 도구 호출 예제
const callMCPTool = async (toolName: string, arguments: any) => {
  const response = await fetch('http://localhost:8000/mcp/tools/call', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      tool_name: toolName,
      arguments: arguments
    })
  });
  return await response.json();
};

// 사용 예제들
const files = await callMCPTool('list_vault_files', { pattern: '*.md' });
const content = await callMCPTool('read_file_content', { file_path: 'note.md' });
const searchResults = await callMCPTool('search_vault', { query: 'python' });
```

### 4. 레거시 엔드포인트 (`/generate`)
**용도**: 기존 호환성을 위한 엔드포인트 (설정에 따라 direct/mcp 모드)
```typescript
// 레거시 요청 (기존 코드와 호환)
const legacyRequest = async (request: AIRequest) => {
  const response = await fetch('http://localhost:8000/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request)
  });
  return await response.json();
};
```

## 설정 관리

### AI 모드 확인
```typescript
const getAIMode = async () => {
  const response = await fetch('http://localhost:8000/config/ai-mode');
  return await response.json();
};
```

### AI 모드 변경
```typescript
const setAIMode = async (mode: 'direct' | 'mcp') => {
  const response = await fetch('http://localhost:8000/config/ai-mode', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(mode)
  });
  return await response.json();
};
```

### API 정보 조회
```typescript
const getAPIInfo = async () => {
  const response = await fetch('http://localhost:8000/api/info');
  return await response.json();
};
```

## Frontend 컴포넌트 예제

```typescript
// AI 요청 타입 정의
type AIRequestType = 'basic' | 'advanced' | 'mcp';

// AI 요청 컴포넌트
class AIRequestManager {
  private baseURL = 'http://localhost:8000';
  
  async requestAI(type: AIRequestType, prompt: string, options?: any) {
    switch (type) {
      case 'basic':
        return this.basicRequest(prompt, options);
      case 'advanced':
        return this.advancedRequest(prompt, options);
      case 'mcp':
        return this.mcpRequest(prompt, options);
      default:
        throw new Error('지원하지 않는 AI 요청 타입입니다.');
    }
  }
  
  private async basicRequest(prompt: string, options?: any) {
    const response = await fetch(`${this.baseURL}/ai/basic/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt,
        provider: options?.provider || 'perplexity',
        model: options?.model || 'gpt-4',
        api_key: options?.api_key
      })
    });
    return await response.json();
  }
  
  private async advancedRequest(prompt: string, options?: any) {
    const response = await fetch(`${this.baseURL}/ai/advanced/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt,
        provider: options?.provider || 'perplexity',
        model: options?.model || 'gpt-4',
        api_key: options?.api_key,
        language: options?.language || 'python'
      })
    });
    return await response.json();
  }
  
  private async mcpRequest(toolName: string, arguments: any) {
    const response = await fetch(`${this.baseURL}/mcp/tools/call`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tool_name: toolName,
        arguments: arguments
      })
    });
    return await response.json();
  }
}

// 사용 예제
const aiManager = new AIRequestManager();

// 기본 질문
const basicAnswer = await aiManager.requestAI('basic', '안녕하세요!');

// 코드 생성
const code = await aiManager.requestAI('advanced', '정렬 알고리즘을 구현해주세요', {
  language: 'python'
});

// 파일 검색
const files = await aiManager.requestAI('mcp', 'list_vault_files', {
  pattern: '*.md'
});
```

## 권장사항

1. **기본 AI 요청**: 사용자가 간단한 질문을 할 때 사용
2. **고급 AI 요청**: 코드 생성이나 구조화된 문서가 필요할 때 사용  
3. **MCP 도구**: 볼트 파일 조작이나 고급 기능이 필요할 때 사용
4. **레거시 엔드포인트**: 기존 코드와의 호환성이 필요할 때만 사용

## 설정 파일

`config.json`에서 AI 모드를 설정할 수 있습니다:
```json
{
  "ai_request_mode": "mcp",
  "providers": {
    // ... provider 설정
  }
}
```

- `"mcp"`: 모든 AI 요청을 MCP 서버를 통해 처리 (권장)
- `"direct"`: 기존 방식대로 AI 엔진을 직접 호출
