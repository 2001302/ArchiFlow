import { ItemView, WorkspaceLeaf, setIcon, MarkdownRenderer, MarkdownView, Notice } from 'obsidian';
import MyPlugin from '../main';
import { VIEW_TYPE_ARCHIFLOW } from './Constants';

export default class ArchiFlowView extends ItemView {
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

		// 상단 바: 다이어그램 선택(토글), Tool Box, Setting
		const topBar = container.createDiv({ cls: 'archiflow-topbar' })
		topBar.style.display = 'flex'
		topBar.style.gap = '8px'
		topBar.style.alignItems = 'center'
		topBar.style.marginBottom = '8px'
		// 깔끔한 토글 버튼 그룹으로 교체
		const toggleGroup = topBar.createDiv({ cls: 'archiflow-toggle-group' })
		toggleGroup.style.display = 'inline-flex'
		toggleGroup.style.border = '1px solid var(--background-modifier-border)'
		toggleGroup.style.borderRadius = '8px'
		toggleGroup.style.overflow = 'hidden'
		const toggleBtn = (label: string) => {
			const btn = toggleGroup.createEl('button', { cls: 'archiflow-btn' })
			btn.textContent = label
			btn.style.padding = '6px 10px'
			btn.style.border = 'none'
			btn.style.background = 'transparent'
			btn.style.cursor = 'pointer'
			btn.style.color = 'var(--text-normal)'
			btn.addClass('archiflow-toggle-item')
			return btn
		}
		const diagramBtn = toggleBtn('Diagram')
		const sourceBtn = toggleBtn('Source')
		const textBtn = toggleBtn('Text')
		const setActive = (active: HTMLButtonElement) => {
			[diagramBtn, sourceBtn, textBtn].forEach(b => {
				if (b === active) {
					b.style.background = 'var(--interactive-accent)'
					b.style.color = 'var(--text-on-accent)'
				} else {
					b.style.background = 'transparent'
					b.style.color = 'var(--text-normal)'
				}
			})
		}
		setActive(diagramBtn)
		diagramBtn.addEventListener('click', () => setActive(diagramBtn))
		sourceBtn.addEventListener('click', () => setActive(sourceBtn))
		textBtn.addEventListener('click', () => setActive(textBtn))
		const toolBoxBtn = topBar.createEl('button', { cls: 'archiflow-btn clickable-icon' })
		toolBoxBtn.setAttr('title', 'Tool Box')
		setIcon(toolBoxBtn, 'wrench')
		const settingBtn = topBar.createEl('button', { cls: 'archiflow-btn clickable-icon' })
		settingBtn.setAttr('title', 'Setting')
		setIcon(settingBtn, 'settings')

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
		footer.style.padding = '8px 40px 8px 8px'
		const prompt = footer.createEl('textarea', { cls: 'prompt-input', placeholder: 'Enter prompt...' })
		prompt.style.width = '100%'
		prompt.style.boxSizing = 'border-box'
		prompt.style.height = '96px'
		// 사용자 크기 조절 비활성화
		;(prompt.style as any).resize = 'none'
		const sendBtn = footer.createEl('button', { cls: 'archiflow-send-btn clickable-icon' })
		sendBtn.style.position = 'absolute'
		sendBtn.style.right = '8px'
		sendBtn.style.bottom = '8px'
		setIcon(sendBtn, 'send')
		// Enter로 전송(Shift+Enter는 줄바꿈)
		prompt.addEventListener('keydown', (ev: KeyboardEvent) => {
			if (ev.key === 'Enter' && !ev.shiftKey) {
				ev.preventDefault()
				sendBtn.click()
			}
		})
		sendBtn.addEventListener('click', async () => {
			const text = (prompt as HTMLTextAreaElement).value
			const block = await addResultBlock(text)
			// 마지막 결과로 자동 스크롤/포커스 이동
			block.scrollIntoView({ behavior: 'smooth', block: 'end' })
			// 전송 후 프롬프트 비우기
			;(prompt as HTMLTextAreaElement).value = ''
		})
	}

	async onClose(): Promise<void> {
		const { contentEl } = this;
		contentEl.empty();
	}
}
