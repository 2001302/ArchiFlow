import { ItemView, WorkspaceLeaf, setIcon, MarkdownRenderer, MarkdownView, Notice } from 'obsidian';
import MyPlugin from '../main';
import { VIEW_TYPE_DOCUMIZE } from './Constants';

// 커스텀 드롭다운 클래스
class CustomDropdown {
	private container: HTMLElement;
	private button: HTMLElement;
	private menu: HTMLElement;
	private options: Array<{ value: string; text: string }>;
	private selectedValue: string;
	private onChangeCallback?: (value: string) => void;
	private isOpen: boolean = false;

	constructor(container: HTMLElement, options: Array<{ value: string; text: string }>, placeholder: string = 'Select...') {
		this.container = container;
		this.options = options;
		this.selectedValue = options[0]?.value || '';
		this.isOpen = false;
		this.createDropdown(placeholder);
	}

	private createDropdown(placeholder: string) {
		// 드롭다운 컨테이너
		this.container.style.position = 'relative';
		this.container.style.display = 'inline-block';

		// 버튼 생성
		this.button = this.container.createDiv({ cls: 'custom-dropdown-button' });
		this.button.style.padding = '4px 8px';
		this.button.style.borderRadius = '8px';
		this.button.style.border = '1px solid var(--background-modifier-border)';
		this.button.style.background = 'var(--background-primary)';
		this.button.style.color = 'var(--text-normal)';
		this.button.style.fontSize = '8px';
		this.button.style.cursor = 'pointer';
		this.button.style.height = '20px';
		this.button.style.display = 'flex';
		this.button.style.alignItems = 'center';
		this.button.style.justifyContent = 'space-between';
		this.button.style.minWidth = '80px';
		this.button.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
		this.button.style.transition = 'all 0.2s ease';

		// 버튼 텍스트
		const buttonText = this.button.createSpan({ cls: 'dropdown-text' });
		buttonText.textContent = this.options[0]?.text || placeholder;

		// 화살표 아이콘
		const arrow = this.button.createSpan({ cls: 'dropdown-arrow' });
		arrow.innerHTML = '▲';
		arrow.style.fontSize = '6px';
		arrow.style.transition = 'transform 0.2s ease';

		// 메뉴 생성
		this.menu = this.container.createDiv({ cls: 'custom-dropdown-menu' });
		this.menu.style.position = 'absolute';
		this.menu.style.top = 'auto';
		this.menu.style.bottom = '100%';
		this.menu.style.left = '0';
		this.menu.style.right = '0';
		this.menu.style.background = 'var(--background-primary)';
		this.menu.style.border = '1px solid var(--background-modifier-border)';
		this.menu.style.borderRadius = '8px';
		this.menu.style.borderTopLeftRadius = '8px';
		this.menu.style.borderTopRightRadius = '8px';
		this.menu.style.borderBottomLeftRadius = '0';
		this.menu.style.borderBottomRightRadius = '0';
		this.menu.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
		this.menu.style.zIndex = '1001';
		this.menu.style.display = 'none';
		this.menu.style.overflow = 'hidden';

		// 옵션들 생성
		this.options.forEach((option, index) => {
			const optionElement = this.menu.createDiv({ cls: 'dropdown-option' });
			optionElement.textContent = option.text;
			optionElement.style.padding = '6px 8px';
			optionElement.style.cursor = 'pointer';
			optionElement.style.fontSize = '8px';
			optionElement.style.color = 'var(--text-normal)';
			optionElement.style.transition = 'background 0.15s ease';
			optionElement.dataset.value = option.value;

			// 호버 효과
			optionElement.addEventListener('mouseenter', () => {
				optionElement.style.background = 'var(--background-modifier-hover)';
			});

			optionElement.addEventListener('mouseleave', () => {
				optionElement.style.background = 'transparent';
			});

			// 클릭 이벤트
			optionElement.addEventListener('click', () => {
				this.selectOption(option.value, option.text);
			});
		});

		// 버튼 클릭 이벤트
		this.button.addEventListener('click', (e) => {
			e.stopPropagation();
			this.toggle();
		});

		// 외부 클릭 시 닫기
		document.addEventListener('click', (e) => {
			if (!this.container.contains(e.target as Node)) {
				this.close();
			}
		});
	}

	private toggle() {
		if (this.isOpen) {
			this.close();
		} else {
			this.open();
		}
	}

	private open() {
		this.isOpen = true;
		this.menu.style.display = 'block';
		this.button.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
		this.button.style.borderColor = 'var(--interactive-accent)';
		
		// 드롭다운 위치 자동 조정
		this.adjustDropdownPosition();
		
		const arrow = this.button.querySelector('.dropdown-arrow') as HTMLElement;
		if (arrow) {
			arrow.style.transform = 'rotate(180deg)';
		}
	}

	private close() {
		this.isOpen = false;
		this.menu.style.display = 'none';
		this.button.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
		this.button.style.borderColor = 'var(--background-modifier-border)';
		
		const arrow = this.button.querySelector('.dropdown-arrow') as HTMLElement;
		if (arrow) {
			arrow.style.transform = 'rotate(0deg)';
		}
	}

	private adjustDropdownPosition() {
		// 항상 위쪽으로만 펼쳐지도록 고정
		if (!this.menu || !this.button) return;

		this.menu.style.top = 'auto';
		this.menu.style.bottom = '100%';
		this.menu.style.borderTopLeftRadius = '8px';
		this.menu.style.borderTopRightRadius = '8px';
		this.menu.style.borderBottomLeftRadius = '0';
		this.menu.style.borderBottomRightRadius = '0';
	}

	private selectOption(value: string, text: string) {
		this.selectedValue = value;
		const buttonText = this.button.querySelector('.dropdown-text') as HTMLElement;
		if (buttonText) {
			buttonText.textContent = text;
		}
		this.close();
		
		if (this.onChangeCallback) {
			this.onChangeCallback(value);
		}
	}

	public getValue(): string {
		return this.selectedValue;
	}

	public setValue(value: string) {
		const option = this.options.find(opt => opt.value === value);
		if (option) {
			this.selectOption(option.value, option.text);
		}
	}

	public onChange(callback: (value: string) => void) {
		this.onChangeCallback = callback;
	}

	public updateOptions(newOptions: Array<{ value: string; text: string }>) {
		this.options = newOptions;
		this.selectedValue = newOptions[0]?.value || '';
		
		// 기존 메뉴 제거
		if (this.menu) {
			this.menu.remove();
		}
		
		// 새 메뉴 생성
		this.menu = this.container.createDiv({ cls: 'custom-dropdown-menu' });
		this.menu.style.position = 'absolute';
		this.menu.style.top = 'auto';
		this.menu.style.bottom = '100%';
		this.menu.style.left = '0';
		this.menu.style.right = '0';
		this.menu.style.background = 'var(--background-primary)';
		this.menu.style.border = '1px solid var(--background-modifier-border)';
		this.menu.style.borderRadius = '8px';
		this.menu.style.borderTopLeftRadius = '8px';
		this.menu.style.borderTopRightRadius = '8px';
		this.menu.style.borderBottomLeftRadius = '0';
		this.menu.style.borderBottomRightRadius = '0';
		this.menu.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
		this.menu.style.zIndex = '1001';
		this.menu.style.display = 'none';
		this.menu.style.overflow = 'hidden';

		// 새 옵션들 생성
		this.options.forEach((option, index) => {
			const optionElement = this.menu.createDiv({ cls: 'dropdown-option' });
			optionElement.textContent = option.text;
			optionElement.style.padding = '6px 8px';
			optionElement.style.cursor = 'pointer';
			optionElement.style.fontSize = '8px';
			optionElement.style.color = 'var(--text-normal)';
			optionElement.style.transition = 'background 0.15s ease';
			optionElement.dataset.value = option.value;

			// 호버 효과
			optionElement.addEventListener('mouseenter', () => {
				optionElement.style.background = 'var(--background-modifier-hover)';
			});

			optionElement.addEventListener('mouseleave', () => {
				optionElement.style.background = 'transparent';
			});

			// 클릭 이벤트
			optionElement.addEventListener('click', () => {
				this.selectOption(option.value, option.text);
			});
		});

		// 버튼 텍스트 업데이트
		const buttonText = this.button.querySelector('.dropdown-text') as HTMLElement;
		if (buttonText) {
			buttonText.textContent = this.options[0]?.text || 'Select...';
		}

		// 드롭다운이 열려있다면 위치 재조정 (약간의 지연을 두어 DOM 업데이트 완료 후 실행)
		if (this.isOpen) {
			// DOM 업데이트가 완료된 후 위치 조정
			setTimeout(() => {
				this.adjustDropdownPosition();
			}, 0);
		}
	}

	public destroy() {
		this.container.empty();
	}
}

export default class SidePannelView extends ItemView {
	private plugin: MyPlugin;

	constructor(leaf: WorkspaceLeaf, plugin: MyPlugin) {
		super(leaf);
		this.plugin = plugin;
	}

	getViewType(): string {
		return VIEW_TYPE_DOCUMIZE;
	}

	getDisplayText(): string {
		return 'documize';
	}

	getIcon(): string {
		return 'dice';
	}

	async onOpen(): Promise<void> {
		const { contentEl } = this
		contentEl.empty()

		// 플러그인 컨테이너 생성
		const pluginContainer = contentEl.createDiv({ 
			cls: 'documize-plugin-root' 
		});
		pluginContainer.style.display = 'flex'
		pluginContainer.style.flexDirection = 'column'
		pluginContainer.style.height = '100%'

		// 라이브러리별 래퍼
		const choicesWrapper = pluginContainer.createDiv({ 
			cls: 'documize-choices-wrapper' 
		});
		choicesWrapper.style.flex = '1 1 auto'
		choicesWrapper.style.overflow = 'auto'
		choicesWrapper.style.padding = '4px'

		const tailwindWrapper = pluginContainer.createDiv({ 
			cls: 'documize-tailwind-wrapper' 
		});
		tailwindWrapper.style.position = 'relative'
		tailwindWrapper.style.padding = '8px'
		tailwindWrapper.style.width = '100%'
		tailwindWrapper.style.boxSizing = 'border-box'

		// CSS 스타일 주입
		this.addStyles();

		// 본문: 결과 리스트 (가득 채움)
		const resultsContainer = choicesWrapper.createDiv({ cls: 'documize-results' })
		resultsContainer.style.display = 'flex'
		resultsContainer.style.flexDirection = 'column'
		resultsContainer.style.gap = '12px'

		// 개별 결과 블록 생성 + 렌더
		const addResultBlock = async (markdown: string): Promise<HTMLDivElement> => {
			const block = resultsContainer.createDiv({ cls: 'documize-result-block' })
			block.style.position = 'relative'
			block.style.border = '1px solid var(--background-modifier-border)'
			block.style.borderRadius = '8px'
			block.style.overflow = 'hidden'

			const header = block.createDiv({ cls: 'documize-result-header' })
			header.style.display = 'flex'
			header.style.justifyContent = 'flex-end'
			header.style.alignItems = 'center'
			header.style.padding = '4px 4px'

			// 액션 버튼들
			const collapseBtn = header.createEl('button', { cls: 'documize-btn clickable-icon' })
			collapseBtn.setAttr('title', 'Collapse / Expand')
			setIcon(collapseBtn, 'chevron-up')

			const editBtn = header.createEl('button', { cls: 'documize-btn clickable-icon' })
			editBtn.setAttr('title', 'Edit')
			setIcon(editBtn, 'pencil')

			const saveBtn = header.createEl('button', { cls: 'documize-btn clickable-icon' })
			saveBtn.setAttr('title', 'Save')
			setIcon(saveBtn, 'check')
			saveBtn.style.display = 'none'

			const applyBtn = header.createEl('button', { cls: 'documize-btn clickable-icon' })
			applyBtn.setAttr('title', 'Apply')
			setIcon(applyBtn, 'corner-down-right')
			applyBtn.style.display = ''

			const copyBtn = header.createEl('button', { cls: 'documize-btn clickable-icon' })
			copyBtn.setAttr('title', 'Copy markdown')
			setIcon(copyBtn, 'copy')

			const bodyEl = block.createDiv({ cls: 'documize-result' })
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
				if (block.hasClass('documize-collapsed')) {
					block.removeClass('documize-collapsed')
					setIcon(collapseBtn, 'chevron-up')
				} else {
					block.addClass('documize-collapsed')
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
		const promptContainer = tailwindWrapper.createDiv({ cls: 'documize-prompt-container' })
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
		const topSection = promptContainer.createDiv({ cls: 'documize-prompt-top' })
		topSection.style.display = 'flex'
		topSection.style.justifyContent = 'space-between'
		topSection.style.alignItems = 'center'
		topSection.style.padding = '8px 8px'
		topSection.style.borderBottom = 'none'
		topSection.style.minHeight = '20px'
		
		// 왼쪽 버튼들
		const leftButtons = topSection.createDiv({ cls: 'documize-left-buttons' })
		leftButtons.style.display = 'flex'
		leftButtons.style.gap = '4px'
		leftButtons.style.alignItems = 'center'
		
		// @아이콘 버튼
		const mentionBtn = leftButtons.createEl('button', { cls: 'documize-mention-btn' })
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
		const attachBtn = leftButtons.createEl('button', { cls: 'documize-attach-btn' })
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
		const middleSection = promptContainer.createDiv({ cls: 'documize-prompt-middle' })
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
		const bottomSection = promptContainer.createDiv({ cls: 'documize-prompt-bottom' })
		bottomSection.style.display = 'flex'
		bottomSection.style.justifyContent = 'space-between'
		bottomSection.style.alignItems = 'center'
		bottomSection.style.padding = '8px 4px'
		bottomSection.style.borderTop = 'none'
		bottomSection.style.minHeight = '30px'
		
		// 왼쪽 컨테이너: mode select와 model select를 함께 배치
		const leftControls = bottomSection.createDiv({ cls: 'documize-left-controls' })
		leftControls.style.display = 'flex'
		leftControls.style.gap = '4px'
		leftControls.style.alignItems = 'center'
		
		// 모드선택 커스텀 드롭다운
		const formatContainer = leftControls.createDiv({ cls: 'documize-format-container' })
		formatContainer.style.position = 'relative'
		formatContainer.style.zIndex = '1000'
		
		// 커스텀 드롭다운 옵션들
		const formatOptions = [
			{ value: 'default', text: 'Select Mode' },
			{ value: 'text', text: 'Chat' },
			{ value: 'document', text: 'Document' }
		]
		
		// 커스텀 드롭다운 생성
		const formatDropdown = new CustomDropdown(formatContainer, formatOptions, 'Select Mode')
		
		// 드롭다운 이벤트 핸들러
		formatDropdown.onChange((selectedValue: string) => {
			// 선택된 모드에 따른 프롬프트 플레이스홀더 변경
			this.updatePromptPlaceholder(selectedValue, prompt as HTMLTextAreaElement);
			
			// documentOption일 때만 template 드랍다운 표시
			if (selectedValue === 'document') {
				templateContainer.style.display = 'block'
			} else {
				templateContainer.style.display = 'none'
			}
		})

		// Select model 커스텀 드롭다운
		const modelContainer = leftControls.createDiv({ cls: 'documize-model-container' })
		modelContainer.style.position = 'relative'
		modelContainer.style.zIndex = '1000'
		
		// 모델 옵션들 (동적으로 로드됨)
		const modelOptions = [
			{ value: 'default', text: 'Select Model' }
		]
		
		// 모델 커스텀 드롭다운 생성
		const modelDropdown = new CustomDropdown(modelContainer, modelOptions, 'Select Model')
		
		// config.json에서 모델 목록 로드
		this.loadModelsFromConfig(modelDropdown)

		// Template type 커스텀 드롭다운 (documentOption일 때만 표시)
		const templateContainer = leftControls.createDiv({ cls: 'documize-template-container' })
		templateContainer.style.position = 'relative'
		templateContainer.style.zIndex = '1000'
		templateContainer.style.display = 'none' // 기본적으로 숨김
		
		// 템플릿 옵션들 (동적으로 로드됨)
		const templateOptions = [
			{ value: 'default', text: 'Select Template' }
		]
		
		// 템플릿 커스텀 드롭다운 생성
		const templateDropdown = new CustomDropdown(templateContainer, templateOptions, 'Select Template')
		
		// templates.json에서 템플릿 목록 로드
		this.loadTemplatesFromConfig(templateDropdown)
		
		// 전송 버튼
		const sendBtn = bottomSection.createEl('button', { cls: 'documize-send-btn clickable-icon' })
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
			const selectedFormat = formatDropdown.getValue() === 'default' ? 'text' : formatDropdown.getValue()

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
	 * CSS 스타일을 동적으로 주입하여 스코핑과 네임스페이싱을 적용
	 */
	private addStyles(): void {
		// 기존 스타일이 있다면 제거
		const existingStyle = document.getElementById('documize-plugin-styles');
		if (existingStyle) {
			existingStyle.remove();
		}

		// 스타일 요소 생성
		const style = document.createElement('style');
		style.id = 'documize-plugin-styles';
		style.textContent = this.getScopedStyles();
		
		// head에 추가
		document.head.appendChild(style);
	}

	/**
	 * 스코핑된 CSS 스타일 반환
	 */
	private getScopedStyles(): string {
		return `
			/* 플러그인 루트 컨테이너 */
			.documize-plugin-root {
				box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
				transition: box-shadow 0.2s ease;
			}

			.documize-plugin-root:hover {
				box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
			}

			/* Choices.js 래퍼 */
			.documize-choices-wrapper {
				/* Choices.js 관련 스타일이 여기에 적용됩니다 */
			}

			/* Tailwind CSS 래퍼 */
			.documize-tailwind-wrapper {
				/* Tailwind CSS 관련 스타일이 여기에 적용됩니다 */
			}

			/* 결과 블록 스타일 */
			.documize-plugin-root .documize-result-block {
				box-shadow: var(--shadow-l);
				background: var(--background-primary);
				position: relative;
				border: 1px solid var(--background-modifier-border);
				border-radius: 8px;
				overflow: hidden;
			}

			.documize-plugin-root .documize-result-header .documize-btn {
				background: transparent;
				border: none;
				padding: 4px;
				border-radius: 6px;
			}

			.documize-plugin-root .documize-result-header .documize-btn:hover {
				background: var(--background-modifier-hover);
			}

			.documize-plugin-root .documize-collapsed .documize-result {
				display: none;
			}

			/* 프롬프트 컨테이너 스타일 */
			.documize-plugin-root .documize-prompt-container {
				transition: all 0.2s ease;
				box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
				position: relative;
				width: 100%;
				border: 1px solid var(--background-modifier-border);
				border-radius: 8px;
				background: var(--background-primary);
				overflow: hidden;
				display: flex;
				flex-direction: column;
				height: 140px;
			}

			.documize-plugin-root .documize-prompt-container:hover {
				box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
			}

			.documize-plugin-root .documize-prompt-container:focus-within {
				border-color: var(--interactive-accent);
				box-shadow: 0 0 0 2px rgba(var(--interactive-accent-rgb), 0.2);
			}

			/* 프롬프트 입력창 스타일 */
			.documize-plugin-root .prompt-input {
				transition: all 0.2s ease;
				width: 100%;
				flex: 1;
				border: none;
				background: transparent;
				color: var(--text-normal);
				font-size: 14px;
				font-family: var(--font-text);
				resize: none;
				outline: none;
				overflow-y: auto;
				overflow-x: hidden;
				line-height: 1.4;
				word-wrap: break-word;
			}

			.documize-plugin-root .prompt-input:focus {
				outline: none;
			}

			.documize-plugin-root .prompt-input::placeholder {
				color: var(--text-muted);
				font-style: italic;
			}

			/* 드롭다운 스타일 */
			.documize-plugin-root .documize-format-select,
			.documize-plugin-root .documize-model-select,
			.documize-plugin-root .documize-template-select {
				transition: all 0.2s ease;
				cursor: pointer;
				padding: 4px 6px;
				border-radius: 12px;
				border: 1px solid var(--background-modifier-border);
				background: var(--background-primary);
				color: var(--text-normal);
				font-size: 8px;
				height: 20px;
				text-align: center;
				text-overflow: ellipsis;
				overflow: hidden;
				white-space: nowrap;
				box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
				position: relative;
				left: 0;
			}

			.documize-plugin-root .documize-format-select:hover,
			.documize-plugin-root .documize-model-select:hover,
			.documize-plugin-root .documize-template-select:hover {
				background: var(--background-modifier-hover) !important;
				transform: translateY(-1px);
				box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
			}

			.documize-plugin-root .documize-format-select:focus,
			.documize-plugin-root .documize-model-select:focus,
			.documize-plugin-root .documize-template-select:focus {
				outline: none;
				border-color: var(--interactive-accent);
				box-shadow: 0 0 0 2px rgba(var(--interactive-accent-rgb), 0.2);
			}

			.documize-plugin-root .documize-format-select option,
			.documize-plugin-root .documize-model-select option,
			.documize-plugin-root .documize-template-select option {
				background: var(--background-primary);
				color: var(--text-normal);
				padding: 8px;
			}

			/* 버튼 스타일 */
			.documize-plugin-root .documize-send-btn {
				transition: all 0.2s ease;
				padding: 6px 8px;
				border-radius: 16px;
				border: 1px solid var(--background-modifier-border);
				background: var(--interactive-accent);
				color: var(--text-on-accent);
				cursor: pointer;
				width: 30px;
				height: 30px;
				display: flex;
				align-items: center;
				justify-content: center;
			}

			.documize-plugin-root .documize-send-btn:hover {
				background: var(--interactive-accent-hover) !important;
				transform: translateY(-1px);
				box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
			}

			.documize-plugin-root .documize-send-btn:active {
				transform: translateY(0);
				box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
			}

			/* 기타 버튼들 */
			.documize-plugin-root .documize-mention-btn,
			.documize-plugin-root .documize-attach-btn {
				padding: 6px;
				border-radius: 6px;
				border: 1px solid var(--background-modifier-border);
				background: var(--background-secondary);
				color: var(--text-normal);
				cursor: pointer;
				display: flex;
				align-items: center;
				justify-content: center;
				width: 24px;
				height: 24px;
			}

			/* 섹션 스타일 */
			.documize-plugin-root .documize-prompt-top,
			.documize-plugin-root .documize-prompt-middle,
			.documize-plugin-root .documize-prompt-bottom {
				display: flex;
				align-items: center;
			}

			.documize-plugin-root .documize-prompt-top {
				justify-content: space-between;
				padding: 8px;
				border-bottom: none;
				min-height: 20px;
			}

			.documize-plugin-root .documize-prompt-middle {
				flex: 1;
				padding: 8px;
				flex-direction: column;
			}

			.documize-plugin-root .documize-prompt-bottom {
				justify-content: space-between;
				padding: 8px 4px;
				border-top: none;
				min-height: 30px;
			}

			.documize-plugin-root .documize-left-buttons,
			.documize-plugin-root .documize-left-controls {
				display: flex;
				gap: 4px;
				align-items: center;
			}

			.documize-plugin-root .documize-format-container,
			.documize-plugin-root .documize-model-container,
			.documize-plugin-root .documize-template-container {
				position: relative;
				z-index: 1000;
			}
		`;
	}

	/**
	 * templates.json에서 템플릿 목록을 로드하여 커스텀 드롭다운에 추가
	 */
	private async loadTemplatesFromConfig(templateDropdown: CustomDropdown): Promise<void> {
		try {
			// 여러 경로 시도
			const possiblePaths = [
				'.obsidian/plugins/documize/templates.json',
				'templates.json',
				'./templates.json'
			];
			
			let templateContent = '';
			let templatePath = '';
			
			// 가능한 경로들을 순서대로 시도
			for (const path of possiblePaths) {
				console.log('시도하는 템플릿 경로:', path);
				if (await this.plugin.app.vault.adapter.exists(path)) {
					templatePath = path;
					templateContent = await this.plugin.app.vault.adapter.read(path);
					console.log('성공적으로 읽은 템플릿 경로:', path);
					break;
				}
			}
			
			if (!templateContent) {
				console.warn('templates.json 파일을 찾을 수 없습니다. 시도한 경로들:', possiblePaths);
				return;
			}
			
			const templateData = JSON.parse(templateContent);
			console.log('로드된 템플릿:', templateData);
			
			// 템플릿 옵션들 생성
			const templateOptions = [
				{ value: 'default', text: 'Select Type' }
			];
			
			// 템플릿 목록 추가
			if (templateData.templates && typeof templateData.templates === 'object') {
				Object.keys(templateData.templates).forEach((templateKey) => {
					templateOptions.push({
						value: templateKey,
						text: templateKey.charAt(0).toUpperCase() + templateKey.slice(1)
					});
				});
				console.log('템플릿 로드 완료:', Object.keys(templateData.templates).length, '개');
			}
			
					// 커스텀 드롭다운에 옵션들 적용
			templateDropdown['options'] = templateOptions;
			templateDropdown['selectedValue'] = 'default';
			templateDropdown['updateOptions'](templateOptions);
			
		} catch (error) {
			console.error('templates.json 로드 실패:', error);
		}
	}

	/**
	 * config.json에서 모델 목록을 로드하여 커스텀 드롭다운에 추가
	 */
	private async loadModelsFromConfig(modelDropdown: CustomDropdown): Promise<void> {
		try {
			// 여러 경로 시도
			const possiblePaths = [
				'.obsidian/plugins/documize/config.json',
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
				return;
			}
			
			const config = JSON.parse(configContent);
			console.log('로드된 config:', config);
			
			// 모델 옵션들 생성
			const modelOptions = [
				{ value: 'default', text: 'Select Model' }
			];
			
			// 모델 목록 추가
			if (config.models && Array.isArray(config.models)) {
				config.models.forEach((model: any) => {
					modelOptions.push({
						value: JSON.stringify({
							name: model.name,
							provider: model.provider,
							model: model.model,
							api_key: model.api_key
						}),
						text: model.name
					});
				});
				console.log('모델 로드 완료:', config.models.length, '개');
			}
			
			// 커스텀 드롭다운에 옵션들 적용
			modelDropdown['options'] = modelOptions;
			modelDropdown['selectedValue'] = 'default';
			modelDropdown['updateOptions'](modelOptions);
			
			// 모델 드롭다운이 열려있다면 위치 재조정
			if (modelDropdown['isOpen']) {
				setTimeout(() => {
					modelDropdown['adjustDropdownPosition']();
				}, 0);
			}
			
		} catch (error) {
			console.error('config.json 로드 실패:', error);
		}
	}

	/**
	 * 현재 선택된 모델 정보를 반환
	 */
	private getCurrentModel(): any | null {
		const modelDropdown = document.querySelector('.documize-model-container .custom-dropdown-button')?.closest('.documize-model-container');
		if (!modelDropdown) {
			return null;
		}
		
		// 커스텀 드롭다운에서 선택된 값 찾기
		const selectedText = modelDropdown.querySelector('.dropdown-text')?.textContent;
		if (!selectedText || selectedText === 'Select Model') {
			return null;
		}
		
		// 선택된 옵션의 value 찾기
		const options = Array.from(modelDropdown.querySelectorAll('.dropdown-option'));
		for (const option of options) {
			if (option.textContent === selectedText) {
				const value = option.getAttribute('data-value');
				if (value && value !== 'default') {
					try {
						return JSON.parse(value);
					} catch (error) {
						console.error('모델 정보 파싱 실패:', error);
						return null;
					}
				}
			}
		}
		
		return null;
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
