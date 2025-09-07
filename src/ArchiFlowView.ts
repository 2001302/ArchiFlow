import { ItemView, WorkspaceLeaf, setIcon } from 'obsidian';
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

		// 상단 바: 다이어그램 선택, Tool Box, Setting
		const topBar = container.createDiv({ cls: 'archiflow-topbar' })
		topBar.style.display = 'flex'
		topBar.style.gap = '8px'
		topBar.style.alignItems = 'center'
		const diagramSelect = topBar.createEl('select', { cls: 'archiflow-diagram-select' })
		;['Diagram', 'Chat'].forEach(name => {
			const opt = diagramSelect.createEl('option')
			opt.value = name
			opt.text = name
		})
		const toolBoxBtn = topBar.createEl('button', { cls: 'archiflow-btn clickable-icon' })
		toolBoxBtn.setAttr('title', 'Tool Box')
		setIcon(toolBoxBtn, 'wrench')
		const settingBtn = topBar.createEl('button', { cls: 'archiflow-btn clickable-icon' })
		settingBtn.setAttr('title', 'Setting')
		setIcon(settingBtn, 'settings')

		// 본문: 결과 영역 (가득 채움)
		const body = container.createDiv({ cls: 'archiflow-body' })
		body.style.flex = '1 1 auto'
		body.style.overflow = 'auto'
		const resultArea = body.createDiv({ cls: 'archiflow-result' })
		resultArea.contentEditable = 'true'
		resultArea.style.height = '100%'

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
	}

	async onClose(): Promise<void> {
		const { contentEl } = this;
		contentEl.empty();
	}
}
