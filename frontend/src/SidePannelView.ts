import { ItemView, WorkspaceLeaf, setIcon, MarkdownRenderer, MarkdownView, Notice } from 'obsidian';
import MyPlugin from '../main';
import { VIEW_TYPE_ARCHIFLOW } from './Constants';

export default class SidePannelView extends ItemView {
	private plugin: MyPlugin;

	constructor(leaf: WorkspaceLeaf, plugin: MyPlugin) {
		super(leaf);
		this.plugin = plugin;
	}

	getViewType(): string {
		return VIEW_TYPE_ARCHIFLOW;
	}

	getDisplayText(): string {
		return 'ArchiFlow';
	}

	getIcon(): string {
		return 'dice';
	}

	async onOpen(): Promise<void> {
		const { contentEl } = this
		contentEl.empty()

		// 루트 컨테이너: 세로 플렉스, 하단 프롬프트 고정
		const container = contentEl.createDiv({ cls: 'archiflow-container' })
		container.style.display = 'flex'
		container.style.flexDirection = 'column'
		container.style.height = '100%'

		// 상단 바 제거 (도구, 설정 버튼 제거)

		// 본문: 결과 리스트 (가득 채움)
		const body = container.createDiv({ cls: 'archiflow-body' })
		body.style.flex = '1 1 auto'
		body.style.overflow = 'auto'
		body.style.padding = '4px'
		const resultsContainer = body.createDiv({ cls: 'archiflow-results' })
		resultsContainer.style.display = 'flex'
		resultsContainer.style.flexDirection = 'column'
		resultsContainer.style.gap = '12px'

		// 개별 결과 블록 생성 + 렌더
		const addResultBlock = async (markdown: string): Promise<HTMLDivElement> => {
			const block = resultsContainer.createDiv({ cls: 'archiflow-result-block' })
			block.style.position = 'relative'
			block.style.border = '1px solid var(--background-modifier-border)'
			block.style.borderRadius = '8px'
			block.style.overflow = 'hidden'

			const header = block.createDiv({ cls: 'archiflow-result-header' })
			header.style.display = 'flex'
			header.style.justifyContent = 'flex-end'
			header.style.alignItems = 'center'
			header.style.padding = '4px 4px'

			// 액션 버튼들
			const collapseBtn = header.createEl('button', { cls: 'archiflow-btn clickable-icon' })
			collapseBtn.setAttr('title', 'Collapse / Expand')
			setIcon(collapseBtn, 'chevron-up')

			const editBtn = header.createEl('button', { cls: 'archiflow-btn clickable-icon' })
			editBtn.setAttr('title', 'Edit')
			setIcon(editBtn, 'pencil')

			const saveBtn = header.createEl('button', { cls: 'archiflow-btn clickable-icon' })
			saveBtn.setAttr('title', 'Save')
			setIcon(saveBtn, 'check')
			saveBtn.style.display = 'none'

			const applyBtn = header.createEl('button', { cls: 'archiflow-btn clickable-icon' })
			applyBtn.setAttr('title', 'Apply')
			setIcon(applyBtn, 'corner-down-right')
			applyBtn.style.display = ''

			const copyBtn = header.createEl('button', { cls: 'archiflow-btn clickable-icon' })
			copyBtn.setAttr('title', 'Copy markdown')
			setIcon(copyBtn, 'copy')

			const bodyEl = block.createDiv({ cls: 'archiflow-result' })
			// 프롬프트와 동일한 여백/가로 폭 느낌
			bodyEl.style.padding = '8px'
			bodyEl.style.boxSizing = 'border-box'
			bodyEl.style.width = '100%'

			let currentMarkdown = markdown || ''
			let isEditing = false

			await MarkdownRenderer.renderMarkdown(currentMarkdown, bodyEl, '', this.plugin)

			// 버튼 표시 로직: 편집 여부에 따라 토글
			const applyEditingState = () => {
				if (isEditing) {
					editBtn.style.display = 'none'
					saveBtn.style.display = ''
					applyBtn.style.display = ''
				} else {
					editBtn.style.display = ''
					saveBtn.style.display = 'none'
					applyBtn.style.display = ''
				}
			}
			applyEditingState()

			// Collapse / Expand
			collapseBtn.addEventListener('click', () => {
				if (block.hasClass('archiflow-collapsed')) {
					block.removeClass('archiflow-collapsed')
					setIcon(collapseBtn, 'chevron-up')
				} else {
					block.addClass('archiflow-collapsed')
					setIcon(collapseBtn, 'chevron-down')
				}
			})

			// Edit: 본문을 textarea로 교체
			editBtn.addEventListener('click', () => {
				if (isEditing) return
				isEditing = true
				bodyEl.empty()
				const textarea = bodyEl.createEl('textarea') as HTMLTextAreaElement
				textarea.value = currentMarkdown
				textarea.style.width = '100%'
				textarea.style.height = '200px'
				textarea.style.boxSizing = 'border-box'
				applyEditingState()
			})

			// Save: textarea 내용을 마크다운으로 렌더
			saveBtn.addEventListener('click', async () => {
				if (!isEditing) return
				const textarea = bodyEl.querySelector('textarea') as HTMLTextAreaElement | null
				if (textarea) {
					currentMarkdown = textarea.value
				}
				isEditing = false
				bodyEl.empty()
				await MarkdownRenderer.renderMarkdown(currentMarkdown, bodyEl, '', this.plugin)
				applyEditingState()
			})

			// Copy: 현재 마크다운을 클립보드로 복사
			copyBtn.addEventListener('click', async () => {
				try {
					await navigator.clipboard.writeText(currentMarkdown)
					new Notice('copied to clipboard.')
				} catch (err) {
					new Notice('failed to copy.')
				}
			})

			// Apply: 현재 마크다운을 활성 에디터에 삽입
			applyBtn.addEventListener('click', () => {
				let mdView = this.app.workspace.getActiveViewOfType(MarkdownView)
				// 현재 활성 뷰가 마크다운이 아니면, 열려있는 마크다운 탭 중 하나를 선택
				if (!mdView) {
					const mdLeaves = this.app.workspace.getLeavesOfType('markdown')
					if (mdLeaves && mdLeaves.length > 0) {
						mdView = mdLeaves[0].view as MarkdownView
					}
				}
				if (!mdView) {
					new Notice('not found markdown view.')
					return
				}
				const editor = mdView.editor
				const textToInsert = currentMarkdown.endsWith('\n') ? currentMarkdown : currentMarkdown + '\n'
				editor.replaceSelection(textToInsert)
				new Notice('inserted answer to the editor.')
			})
			return block
		}


		// 하단 프롬프트 바: 항상 하단, 가로 꽉 채움
		const footer = container.createDiv({ cls: 'archiflow-footer' })
		footer.style.position = 'relative'
		footer.style.padding = '8px'
		footer.style.width = '100%'
		footer.style.boxSizing = 'border-box'
		
		// 프롬프트 입력 컨테이너
		const promptContainer = footer.createDiv({ cls: 'archiflow-prompt-container' })
		promptContainer.style.position = 'relative'
		promptContainer.style.width = '100%'
		promptContainer.style.border = '1px solid var(--background-modifier-border)'
		promptContainer.style.borderRadius = '8px'
		promptContainer.style.background = 'var(--background-primary)'
		promptContainer.style.overflow = 'hidden'
		
		// 출력 형식 드랍다운 (좌상단)
		const formatContainer = promptContainer.createDiv({ cls: 'archiflow-format-container' })
		formatContainer.style.position = 'absolute'
		formatContainer.style.left = '8px'
		formatContainer.style.top = '8px'
		formatContainer.style.zIndex = '10'
		
		const formatSelect = formatContainer.createEl('select', { cls: 'archiflow-format-select' })
		formatSelect.style.padding = '6px 8px 6px 28px' // 왼쪽에 아이콘 공간 확보
		formatSelect.style.borderRadius = '6px'
		formatSelect.style.border = '1px solid var(--background-modifier-border)'
		formatSelect.style.background = 'var(--background-secondary)'
		formatSelect.style.color = 'var(--text-normal)'
		formatSelect.style.fontSize = '12px'
		formatSelect.style.cursor = 'pointer'
		formatSelect.style.minWidth = '80px'
		
		// 모드별 아이콘 매핑
		const modeIcons = {
			'mermaid': 'git-branch',
			'source_code': 'code',
			'text': 'file-text'
		}
		
		const diagramOption = formatSelect.createEl('option', { value: 'mermaid' })
		diagramOption.textContent = 'Diagram'
		const sourceOption = formatSelect.createEl('option', { value: 'source_code' })
		sourceOption.textContent = 'Source'
		const textOption = formatSelect.createEl('option', { value: 'text' })
		textOption.textContent = 'Text'
		textOption.selected = true // 기본값
		
		// 모드 아이콘 표시
		const modeIcon = formatContainer.createEl('span', { cls: 'archiflow-mode-icon' })
		modeIcon.style.position = 'absolute'
		modeIcon.style.left = '8px'
		modeIcon.style.top = '50%'
		modeIcon.style.transform = 'translateY(-50%)'
		modeIcon.style.pointerEvents = 'none'
		modeIcon.style.fontSize = '14px'
		modeIcon.style.color = 'var(--text-muted)'
		setIcon(modeIcon, modeIcons['text'])
		
		// 드랍다운 상태에 따른 아이콘 업데이트
		formatSelect.addEventListener('change', () => {
			const selectedValue = formatSelect.value as keyof typeof modeIcons
			setIcon(modeIcon, modeIcons[selectedValue])
		})
		
		// Test 버튼 (우상단)
		const testBtn = promptContainer.createEl('button', { cls: 'archiflow-test-btn' })
		testBtn.style.position = 'absolute'
		testBtn.style.right = '8px'
		testBtn.style.top = '8px'
		testBtn.style.padding = '6px 12px'
		testBtn.style.borderRadius = '6px'
		testBtn.style.border = '1px solid var(--background-modifier-border)'
		testBtn.style.background = 'var(--background-secondary)'
		testBtn.style.color = 'var(--text-normal)'
		testBtn.style.fontSize = '12px'
		testBtn.style.cursor = 'pointer'
		testBtn.style.zIndex = '10'
		testBtn.textContent = 'Test'
		
		// Send 버튼 (우하단)
		const sendBtn = promptContainer.createEl('button', { cls: 'archiflow-send-btn clickable-icon' })
		sendBtn.style.position = 'absolute'
		sendBtn.style.right = '8px'
		sendBtn.style.bottom = '8px'
		sendBtn.style.padding = '8px'
		sendBtn.style.borderRadius = '6px'
		sendBtn.style.border = '1px solid var(--background-modifier-border)'
		sendBtn.style.background = 'var(--interactive-accent)'
		sendBtn.style.color = 'var(--text-on-accent)'
		sendBtn.style.cursor = 'pointer'
		sendBtn.style.zIndex = '10'
		setIcon(sendBtn, 'send')
		
		// 프롬프트 입력창
		const prompt = promptContainer.createEl('textarea', { cls: 'prompt-input', placeholder: 'Enter prompt...' })
		prompt.style.width = '100%'
		prompt.style.boxSizing = 'border-box'
		prompt.style.height = '96px'
		prompt.style.padding = '40px 80px 40px 8px' // 상단과 우측에 버튼 공간 확보
		prompt.style.border = 'none'
		prompt.style.background = 'transparent'
		prompt.style.color = 'var(--text-normal)'
		prompt.style.fontSize = '14px'
		prompt.style.fontFamily = 'var(--font-text)'
		prompt.style.resize = 'none'
		prompt.style.outline = 'none'
		// Test 버튼 클릭 이벤트
		testBtn.addEventListener('click', async () => {
			const text = (prompt as HTMLTextAreaElement).value.trim()
			if (!text) return

			// 선택된 출력 형식 가져오기
			const selectedFormat = (formatSelect as HTMLSelectElement).value

			// 로딩 상태 표시
			const loadingBlock = await addResultBlock('Test 모드: 프롬프트를 처리하고 있습니다...')
			loadingBlock.style.opacity = '0.7'

			try {
				// Test 모드: 프롬프트 내용을 그대로 결과창에 표시
				const testResponse = `**Test 모드 결과**\n\n**입력된 프롬프트:**\n${text}\n\n**선택된 출력 형식:** ${selectedFormat}\n\n*이것은 Test 모드입니다. 실제 AI 응답이 아닙니다.*`
				
				// 로딩 블록 제거
				loadingBlock.remove()
				
				// Test 결과 표시
				const resultBlock = await addResultBlock(testResponse)
				resultBlock.scrollIntoView({ behavior: 'smooth', block: 'end' })
			} catch (error) {
				// 로딩 블록 제거
				loadingBlock.remove()
				
				// 에러 표시
				const errorBlock = await addResultBlock(`Test 모드 오류: ${error.message}`)
				errorBlock.style.borderColor = 'var(--text-error)'
				errorBlock.scrollIntoView({ behavior: 'smooth', block: 'end' })
			}
		})

		// Enter로 전송(Shift+Enter는 줄바꿈)
		prompt.addEventListener('keydown', (ev: KeyboardEvent) => {
			if (ev.key === 'Enter' && !ev.shiftKey) {
				ev.preventDefault()
				sendBtn.click()
			}
		})
		sendBtn.addEventListener('click', async () => {
			const text = (prompt as HTMLTextAreaElement).value.trim()
			if (!text) return

			// API Key 확인
			const apiKey = this.getCurrentApiKey()
			if (!apiKey) {
				new Notice('API Key가 설정되지 않았습니다. 설정에서 API Key를 입력해주세요.')
				return
			}

			// 선택된 출력 형식 가져오기
			const selectedFormat = (formatSelect as HTMLSelectElement).value

			// 로딩 상태 표시
			const loadingBlock = await addResultBlock('AI 응답을 생성하고 있습니다...')
			loadingBlock.style.opacity = '0.7'

			try {
				// AI 요청
				const aiResponse = await this.sendAIRequest(text, apiKey, selectedFormat)
				
				// 로딩 블록 제거
				loadingBlock.remove()
				
				// AI 응답 표시
				const resultBlock = await addResultBlock(aiResponse)
				resultBlock.scrollIntoView({ behavior: 'smooth', block: 'end' })
			} catch (error) {
				// 로딩 블록 제거
				loadingBlock.remove()
				
				// 에러 표시
				const errorBlock = await addResultBlock(`오류가 발생했습니다: ${error.message}`)
				errorBlock.style.borderColor = 'var(--text-error)'
				errorBlock.scrollIntoView({ behavior: 'smooth', block: 'end' })
			}

			// 전송 후 프롬프트 비우기
			;(prompt as HTMLTextAreaElement).value = ''
		})
	}

	async onClose(): Promise<void> {
		const { contentEl } = this;
		contentEl.empty();
	}

	/**
	 * 현재 선택된 AI 제공자의 API Key를 반환
	 */
	private getCurrentApiKey(): string | null {
		const provider = this.plugin.settings.selectedProvider
		switch (provider) {
			case 'perplexity':
				return this.plugin.settings.perplexityApiKey || null
			case 'openai':
				return this.plugin.settings.openaiApiKey || null
			case 'anthropic':
				return this.plugin.settings.anthropicApiKey || null
			default:
				return null
		}
	}

	/**
	 * 백그라운드 서버에 AI 요청을 전송
	 */
	private async sendAIRequest(prompt: string, apiKey: string, outputFormat: string = 'text'): Promise<string> {
		const serverUrl = 'http://localhost:8000' // 백그라운드 서버 URL
		
		const requestBody = {
			prompt: prompt,
			output_format: outputFormat,
			provider: this.plugin.settings.selectedProvider,
			api_key: apiKey // API Key를 요청에 포함
		}

		try {
			const response = await fetch(`${serverUrl}/generate`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(requestBody)
			})

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({}))
				throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
			}

			const data = await response.json()
			
			if (!data.success) {
				throw new Error(data.error || 'AI 응답 생성에 실패했습니다.')
			}

			return data.content || '응답이 비어있습니다.'
		} catch (error) {
			if (error instanceof TypeError && error.message.includes('fetch')) {
				throw new Error('백그라운드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.')
			}
			throw error
		}
	}
}
