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
		
		// 프롬프트 입력 컨테이너 - 세 구역으로 나누기
		const promptContainer = footer.createDiv({ cls: 'archiflow-prompt-container' })
		promptContainer.style.position = 'relative'
		promptContainer.style.width = '100%'
		promptContainer.style.border = '1px solid var(--background-modifier-border)'
		promptContainer.style.borderRadius = '8px'
		promptContainer.style.background = 'var(--background-primary)'
		promptContainer.style.overflow = 'hidden'
		promptContainer.style.display = 'flex'
		promptContainer.style.flexDirection = 'column'
		promptContainer.style.height = '140px' // 세로 크기 증가
		
		// 1. 상단 구역: @아이콘 버튼, 파일 첨부 버튼, 테스트 버튼
		const topSection = promptContainer.createDiv({ cls: 'archiflow-prompt-top' })
		topSection.style.display = 'flex'
		topSection.style.justifyContent = 'space-between'
		topSection.style.alignItems = 'center'
		topSection.style.padding = '8px 8px'
		topSection.style.borderBottom = 'none'
		topSection.style.minHeight = '20px'
		
		// 왼쪽 버튼들
		const leftButtons = topSection.createDiv({ cls: 'archiflow-left-buttons' })
		leftButtons.style.display = 'flex'
		leftButtons.style.gap = '4px'
		leftButtons.style.alignItems = 'center'
		
		// @아이콘 버튼
		const mentionBtn = leftButtons.createEl('button', { cls: 'archiflow-mention-btn' })
		mentionBtn.style.padding = '6px'
		mentionBtn.style.borderRadius = '6px'
		mentionBtn.style.border = '1px solid var(--background-modifier-border)'
		mentionBtn.style.background = 'var(--background-secondary)'
		mentionBtn.style.color = 'var(--text-normal)'
		mentionBtn.style.cursor = 'pointer'
		mentionBtn.style.display = 'flex'
		mentionBtn.style.alignItems = 'center'
		mentionBtn.style.justifyContent = 'center'
		mentionBtn.style.width = '24px'
		mentionBtn.style.height = '24px'
		setIcon(mentionBtn, 'at-sign')
		
		// 파일 첨부 버튼
		const attachBtn = leftButtons.createEl('button', { cls: 'archiflow-attach-btn' })
		attachBtn.style.padding = '6px'
		attachBtn.style.borderRadius = '6px'
		attachBtn.style.border = '1px solid var(--background-modifier-border)'
		attachBtn.style.background = 'var(--background-secondary)'
		attachBtn.style.color = 'var(--text-normal)'
		attachBtn.style.cursor = 'pointer'
		attachBtn.style.display = 'flex'
		attachBtn.style.alignItems = 'center'
		attachBtn.style.justifyContent = 'center'
		attachBtn.style.width = '24px'
		attachBtn.style.height = '24px'
		setIcon(attachBtn, 'paperclip')
		
		// 2. 중간 구역: 프롬프트 입력창
		const middleSection = promptContainer.createDiv({ cls: 'archiflow-prompt-middle' })
		middleSection.style.flex = '1'
		middleSection.style.padding = '8px 8px'
		middleSection.style.display = 'flex'
		middleSection.style.flexDirection = 'column'
		
		const prompt = middleSection.createEl('textarea', { cls: 'prompt-input', placeholder: '질문이나 요청을 입력해주세요. 예: "React와 Vue의 차이점을 설명해줘"' })
		prompt.style.width = '100%'
		prompt.style.flex = '1'
		prompt.style.border = 'none'
		prompt.style.background = 'transparent'
		prompt.style.color = 'var(--text-normal)'
		prompt.style.fontSize = '14px'
		prompt.style.fontFamily = 'var(--font-text)'
		prompt.style.resize = 'none'
		prompt.style.outline = 'none'
		prompt.style.overflowY = 'auto'
		prompt.style.overflowX = 'hidden'
		prompt.style.lineHeight = '1.4'
		prompt.style.wordWrap = 'break-word'
		
		// 3. 하단 구역: 모드선택 드롭다운, model select, 전송 버튼
		const bottomSection = promptContainer.createDiv({ cls: 'archiflow-prompt-bottom' })
		bottomSection.style.display = 'flex'
		bottomSection.style.justifyContent = 'space-between'
		bottomSection.style.alignItems = 'center'
		bottomSection.style.padding = '8px 4px'
		bottomSection.style.borderTop = 'none'
		bottomSection.style.minHeight = '30px'
		
		// 왼쪽 컨테이너: mode select와 model select를 함께 배치
		const leftControls = bottomSection.createDiv({ cls: 'archiflow-left-controls' })
		leftControls.style.display = 'flex'
		leftControls.style.gap = '4px'
		leftControls.style.alignItems = 'center'
		
		// 모드선택 드롭다운
		const formatContainer = leftControls.createDiv({ cls: 'archiflow-format-container' })
		formatContainer.style.position = 'relative'
		formatContainer.style.zIndex = '1000'
		
		const formatSelect = formatContainer.createEl('select', { cls: 'archiflow-format-select' })
		formatSelect.style.padding = '4px 6px'
		formatSelect.style.borderRadius = '12px'
		formatSelect.style.border = '1px solid var(--background-modifier-border)'
		formatSelect.style.background = 'var(--background-primary)'
		formatSelect.style.color = 'var(--text-normal)'
		formatSelect.style.fontSize = '8px'
		formatSelect.style.cursor = 'pointer'
		formatSelect.style.height = '20px'
		formatSelect.style.textAlign = 'center'
		formatSelect.style.textOverflow = 'ellipsis'
		formatSelect.style.overflow = 'hidden'
		formatSelect.style.whiteSpace = 'nowrap'
		formatSelect.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)'
		formatSelect.style.transition = 'width 0.2s ease, min-width 0.2s ease, box-shadow 0.2s ease, background 0.2s ease'
		// 좌측 정렬을 위해 left: 0 설정
		formatSelect.style.position = 'relative'
		formatSelect.style.left = '0'
		
		// 기본 옵션 추가
		const defaultOption = formatSelect.createEl('option', { value: 'default' })
		defaultOption.textContent = 'Select Mode'
		defaultOption.selected = true
		
		const textOption = formatSelect.createEl('option', { value: 'text' })
		textOption.textContent = 'Text'
		const documentOption = formatSelect.createEl('option', { value: 'document' })
		documentOption.textContent = 'Document'
		
		// 텍스트 크기에 맞춰 드롭다운 너비 조정 함수
		const adjustFormatSelectWidth = () => {
			const selectedOption = formatSelect.options[formatSelect.selectedIndex]
			if (selectedOption && selectedOption.textContent) {
				const textWidth = selectedOption.textContent.length * 6 + 12 // 대략적인 텍스트 너비 계산
				const maxWidth = 80 // 최대 너비 설정
				formatSelect.style.width = `${Math.min(textWidth, maxWidth)}px`
				formatSelect.style.minWidth = `${Math.min(textWidth, maxWidth)}px`
			}
		}
		
		// 초기 너비 설정
		adjustFormatSelectWidth()
		
		// 드랍다운 이벤트
		formatSelect.addEventListener('change', () => {
			const selectedValue = formatSelect.value;
			
			// 선택된 모드에 따른 프롬프트 플레이스홀더 변경
			this.updatePromptPlaceholder(selectedValue, prompt as HTMLTextAreaElement);
			
			// 너비 재조정
			setTimeout(() => {
				adjustFormatSelectWidth()
			}, 100)
		})
		
		formatSelect.addEventListener('mousedown', () => {
			// 드롭다운이 열릴 때 위치 조정 - 좌측 정렬 유지
			const rect = formatSelect.getBoundingClientRect()
			const containerRect = promptContainer.getBoundingClientRect()
			const spaceAbove = rect.top - containerRect.top
			const spaceBelow = containerRect.bottom - rect.bottom
			
			// 좌측 정렬 유지하면서 위치만 조정
			formatSelect.style.left = '0'
			formatSelect.style.transform = 'none'
			
			// 위쪽 공간이 더 많으면 위로, 아래쪽 공간이 더 많으면 아래로
			if (spaceAbove > spaceBelow) {
				formatSelect.style.transform = 'translateY(-4px)'
			} else {
				formatSelect.style.transform = 'translateY(4px)'
			}
			
			formatSelect.style.width = '80px'
			formatSelect.style.minWidth = '80px'
			formatSelect.style.background = 'var(--background-primary)'
			formatSelect.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)'
		})
		
		formatSelect.addEventListener('blur', () => {
			formatSelect.style.transform = 'translateY(0)'
			formatSelect.style.left = '0'
			formatSelect.style.background = 'var(--background-primary)'
			formatSelect.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)'
			adjustFormatSelectWidth()
		})

		// Select model 드롭다운
		const modelContainer = leftControls.createDiv({ cls: 'archiflow-model-container' })
		modelContainer.style.position = 'relative'
		modelContainer.style.zIndex = '1000'
		
		const modelSelect = modelContainer.createEl('select', { cls: 'archiflow-model-select' })
		modelSelect.style.padding = '4px 6px'
		modelSelect.style.borderRadius = '12px'
		modelSelect.style.border = '1px solid var(--background-modifier-border)'
		modelSelect.style.background = 'var(--background-primary)'
		modelSelect.style.color = 'var(--text-normal)'
		modelSelect.style.fontSize = '8px'
		modelSelect.style.cursor = 'pointer'
		modelSelect.style.height = '20px'
		modelSelect.style.textAlign = 'center'
		modelSelect.style.textOverflow = 'ellipsis'
		modelSelect.style.overflow = 'hidden'
		modelSelect.style.whiteSpace = 'nowrap'
		modelSelect.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)'
		modelSelect.style.transition = 'width 0.2s ease, min-width 0.2s ease, box-shadow 0.2s ease, background 0.2s ease'
		// 좌측 정렬을 위해 left: 0 설정
		modelSelect.style.position = 'relative'
		modelSelect.style.left = '0'
		
		
		// 텍스트 크기에 맞춰 모델 드롭다운 너비 조정 함수
		const adjustModelSelectWidth = () => {
			const selectedOption = modelSelect.options[modelSelect.selectedIndex]
			if (selectedOption && selectedOption.textContent) {
				const textWidth = selectedOption.textContent.length * 6 + 12 // 대략적인 텍스트 너비 계산
				const maxWidth = 100 // 최대 너비 설정
				modelSelect.style.width = `${Math.min(textWidth, maxWidth)}px`
				modelSelect.style.minWidth = `${Math.min(textWidth, maxWidth)}px`
			}
		}
		
		// config.json에서 모델 목록 로드
		this.loadModelsFromConfig(modelSelect).then(() => {
			// 초기 로드 후 너비 설정
			adjustModelSelectWidth()
		})
		
		// 모델 선택 이벤트
		modelSelect.addEventListener('mousedown', () => {
			// 드롭다운이 열릴 때 위치 조정 - 좌측 정렬 유지
			const rect = modelSelect.getBoundingClientRect()
			const containerRect = promptContainer.getBoundingClientRect()
			const spaceAbove = rect.top - containerRect.top
			const spaceBelow = containerRect.bottom - rect.bottom
			
			// 좌측 정렬 유지하면서 위치만 조정
			modelSelect.style.left = '0'
			modelSelect.style.transform = 'none'
			
			// 위쪽 공간이 더 많으면 위로, 아래쪽 공간이 더 많으면 아래로
			if (spaceAbove > spaceBelow) {
				modelSelect.style.transform = 'translateY(-4px)'
			} else {
				modelSelect.style.transform = 'translateY(4px)'
			}
			
			modelSelect.style.width = '120px'
			modelSelect.style.minWidth = '120px'
			modelSelect.style.background = 'var(--background-primary)'
			modelSelect.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)'
		})
		
		modelSelect.addEventListener('blur', () => {
			modelSelect.style.transform = 'translateY(0)'
			modelSelect.style.left = '0'
			modelSelect.style.background = 'var(--background-primary)'
			modelSelect.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)'
			adjustModelSelectWidth()
		})
		
		modelSelect.addEventListener('change', () => {
			setTimeout(() => {
				adjustModelSelectWidth()
			}, 100)
		})
		
		// 전송 버튼
		const sendBtn = bottomSection.createEl('button', { cls: 'archiflow-send-btn clickable-icon' })
		sendBtn.style.padding = '6px 8px'
		sendBtn.style.borderRadius = '16px'
		sendBtn.style.border = '1px solid var(--background-modifier-border)'
		sendBtn.style.background = 'var(--interactive-accent)'
		sendBtn.style.color = 'var(--text-on-accent)'
		sendBtn.style.cursor = 'pointer'
		sendBtn.style.width = '30px'
		sendBtn.style.height = '30px'
		sendBtn.style.display = 'flex'
		sendBtn.style.alignItems = 'center'
		sendBtn.style.justifyContent = 'center'
		setIcon(sendBtn, 'send')

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

			// 선택된 모델 확인
			const selectedModel = this.getCurrentModel()
			if (!selectedModel) {
				new Notice('모델이 선택되지 않았습니다. config.json에서 모델을 설정해주세요.')
				return
			}

			// 선택된 출력 형식 가져오기
			const selectedFormat = (formatSelect as HTMLSelectElement).value === 'default' ? 'text' : (formatSelect as HTMLSelectElement).value

			// 로딩 상태 표시
			const loadingBlock = await addResultBlock('AI 응답을 생성하고 있습니다...')
			loadingBlock.style.opacity = '0.7'

			try {
				// AI 요청
				const aiResponse = await this.sendAIRequest(text, selectedModel, selectedFormat)
				
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
	 * config.json에서 모델 목록을 로드하여 드롭다운에 추가
	 */
	private async loadModelsFromConfig(modelSelect: HTMLSelectElement): Promise<void> {
		try {
			// 여러 경로 시도
			const possiblePaths = [
				'.obsidian/plugins/arch-flow/config.json',
				'config.json',
				'./config.json'
			];
			
			let configContent = '';
			let configPath = '';
			
			// 가능한 경로들을 순서대로 시도
			for (const path of possiblePaths) {
				console.log('시도하는 경로:', path);
				if (await this.plugin.app.vault.adapter.exists(path)) {
					configPath = path;
					configContent = await this.plugin.app.vault.adapter.read(path);
					console.log('성공적으로 읽은 경로:', path);
					break;
				}
			}
			
			if (!configContent) {
				console.warn('config.json 파일을 찾을 수 없습니다. 시도한 경로들:', possiblePaths);
				// 기본 모델 추가
				const defaultOption = modelSelect.createEl('option', { value: 'default' });
				defaultOption.textContent = 'Select Model';
				return;
			}
			
			const config = JSON.parse(configContent);
			console.log('로드된 config:', config);
			
			// 기존 옵션 제거
			modelSelect.innerHTML = '';
			
			// 기본 옵션 추가
			const defaultOption = modelSelect.createEl('option', { value: 'default' });
			defaultOption.textContent = 'Select Model';
			defaultOption.selected = true;
			
			// 모델 목록 추가
			if (config.models && Array.isArray(config.models)) {
				config.models.forEach((model: any) => {
					const option = modelSelect.createEl('option', { 
						value: JSON.stringify({
							name: model.name,
							provider: model.provider,
							model: model.model,
							api_key: model.api_key
						})
					});
					option.textContent = model.name;
				});
				console.log('모델 로드 완료:', config.models.length, '개');
			}
		} catch (error) {
			console.error('config.json 로드 실패:', error);
			// 에러 시 기본 모델 추가
			modelSelect.innerHTML = '';
			const defaultOption = modelSelect.createEl('option', { value: 'default' });
			defaultOption.textContent = 'Select Model';
		}
	}

	/**
	 * 현재 선택된 모델 정보를 반환
	 */
	private getCurrentModel(): any | null {
		const modelSelect = document.querySelector('.archiflow-model-select') as HTMLSelectElement;
		if (!modelSelect || modelSelect.value === 'default') {
			return null;
		}
		
		try {
			return JSON.parse(modelSelect.value);
		} catch (error) {
			console.error('모델 정보 파싱 실패:', error);
			return null;
		}
	}

	/**
	 * 출력 형식에 따른 요청 바디 구성
	 */
	private buildRequestByFormat(prompt: string, outputFormat: string, model: any): any {
		const baseRequest = {
			prompt: prompt,
			output_format: outputFormat,
			provider: model.provider,
			model: model.model,
			api_key: model.api_key
		}

		return baseRequest
	}


	/**
	 * 프롬프트에서 프로그래밍 언어 감지
	 */
	private detectLanguage(prompt: string): string | null {
		const languageKeywords = {
			'python': ['python', 'py', 'pandas', 'numpy', 'django', 'flask'],
			'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular'],
			'typescript': ['typescript', 'ts', 'interface', 'type'],
			'java': ['java', 'spring', 'maven', 'gradle'],
			'cpp': ['cpp', 'c++', 'stl', 'vector', 'map'],
			'c': ['c언어', 'c language', 'stdio', 'stdlib'],
			'go': ['go', 'golang', 'goroutine', 'channel'],
			'rust': ['rust', 'cargo', 'ownership', 'borrow'],
			'php': ['php', 'laravel', 'symfony', 'composer'],
			'ruby': ['ruby', 'rails', 'gem', 'bundle'],
			'swift': ['swift', 'ios', 'xcode', 'cocoa'],
			'kotlin': ['kotlin', 'android', 'gradle'],
			'sql': ['sql', 'database', 'select', 'insert', 'update', 'delete'],
			'html': ['html', 'div', 'span', 'class', 'id'],
			'css': ['css', 'style', 'margin', 'padding', 'color'],
			'bash': ['bash', 'shell', 'script', 'terminal', 'command'],
			'powershell': ['powershell', 'ps1', 'cmdlet']
		}

		const lowerPrompt = prompt.toLowerCase()
		for (const [language, keywords] of Object.entries(languageKeywords)) {
			if (keywords.some(keyword => lowerPrompt.includes(keyword))) {
				return language
			}
		}
		
		return null
	}

	/**
	 * 선택된 모드에 따른 프롬프트 플레이스홀더 업데이트
	 */
	private updatePromptPlaceholder(format: string, promptElement: HTMLTextAreaElement): void {
		const placeholders: Record<string, string> = {
			'document': 'create a document',
			'text': 'ask a question or request',
			'default': 'ask a question or request'
		}
		
		promptElement.placeholder = placeholders[format] || placeholders['text']
	}

	/**
	 * 백그라운드 서버에 AI 요청을 전송
	 */
	private async sendAIRequest(prompt: string, model: any, outputFormat: string = 'text'): Promise<string> {
		// 백엔드가 실행 중인지 확인하고 필요시 시작
		const isBackendReady = await (this.plugin as any).ensureBackendRunning();
		if (!isBackendReady) {
			throw new Error('Backend 서버를 시작할 수 없습니다. 설정을 확인해주세요.');
		}

		const backendManager = this.plugin.getBackendManager();
		const serverUrl = backendManager.getServerUrl();
		
		// 서버가 실제로 응답하는지 한 번 더 확인
		const isServerHealthy = await backendManager.isServerRunning();
		if (!isServerHealthy) {
			throw new Error('Backend 서버가 응답하지 않습니다. 잠시 후 다시 시도해주세요.');
		}
		
		// 출력 형식에 따른 추가 파라미터 설정
		const requestBody = this.buildRequestByFormat(prompt, outputFormat, model)

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
			if (error.name === 'AbortError') {
				throw new Error('요청이 시간 초과되었습니다. 네트워크 연결을 확인해주세요.')
			}
			if (error.message.includes('Backend 서버를 시작할 수 없습니다')) {
				throw error // 이미 적절한 메시지가 있음
			}
			if (error.message.includes('Backend 서버가 응답하지 않습니다')) {
				throw error // 이미 적절한 메시지가 있음
			}
			throw error
		}
	}
}
