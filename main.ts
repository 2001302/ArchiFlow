import { Editor, MarkdownView, Notice, Plugin, MarkdownPostProcessorContext, setIcon } from 'obsidian';
import { VIEW_TYPE_ARCHIFLOW } from './src/Constants';
import { MyPluginSettings, DEFAULT_SETTINGS } from './src/Settings';
import SidePannelView from './src/SidePannelView';
import SampleModal from './src/SampleModal';
import SampleSettingTab from './src/SampleSettingTab';
import { CodeBlockProcessor } from './src/CodeBlock';

export default class MyPlugin extends Plugin {
	settings: MyPluginSettings;
	private codeBlockProcessor: CodeBlockProcessor;

	async onload() {
		await this.loadSettings();

		// Initialize code block processor
		this.codeBlockProcessor = new CodeBlockProcessor(this.app);

		// Register right panel view
		this.registerView(VIEW_TYPE_ARCHIFLOW, (leaf) => new SidePannelView(leaf, this));

		// Command to open the right panel
		this.addCommand({
			id: 'open-archiflow-panel',
			name: 'Open ArchiFlow panel',
			callback: async () => {
				await this.activateRightPanel();
			}
		});

		// Left ribbon icon to open the right panel directly
		const ribbonIconEl = this.addRibbonIcon('dice', 'open ArchiFlow panel', async (evt: MouseEvent) => {
			await this.activateRightPanel();
		});
		// Perform additional things with the ribbon
		ribbonIconEl.addClass('my-plugin-ribbon-class');

		// This adds a status bar item to the bottom of the app. Does not work on mobile apps.
		const statusBarItemEl = this.addStatusBarItem();
		statusBarItemEl.setText('Status Bar Text');

		// This adds a simple command that can be triggered anywhere
		this.addCommand({
			id: 'open-sample-modal-simple',
			name: 'Open sample modal (simple)',
			callback: () => {
				new SampleModal(this.app).open();
			}
		});
		// This adds an editor command that can perform some operation on the current editor instance
		this.addCommand({
			id: 'sample-editor-command',
			name: 'Sample editor command',
			editorCallback: (editor: Editor, view: MarkdownView) => {
				console.log(editor.getSelection());
				editor.replaceSelection('Sample Editor Command');
			}
		});
		// This adds a complex command that can check whether the current state of the app allows execution of the command
		this.addCommand({
			id: 'open-sample-modal-complex',
			name: 'Open sample modal (complex)',
			checkCallback: (checking: boolean) => {
				// Conditions to check
				const markdownView = this.app.workspace.getActiveViewOfType(MarkdownView);
				if (markdownView) {
					// If checking is true, we're simply "checking" if the command can be run.
					// If checking is false, then we want to actually perform the operation.
					if (!checking) {
						new SampleModal(this.app).open();
					}

					// This command will only show up in Command Palette when the check function returns true
					return true;
				}
			}
		});

		// Register markdown code block processor for arch-flow code blocks
		this.registerMarkdownCodeBlockProcessor('arch-flow', this.codeBlockProcessor.processArchFlowCodeBlock.bind(this.codeBlockProcessor));

		// This adds a settings tab so the user can configure various aspects of the plugin
		this.addSettingTab(new SampleSettingTab(this.app, this));

		// If the plugin hooks up any global DOM events (on parts of the app that doesn't belong to this plugin)
		// Using this function will automatically remove the event listener when this plugin is disabled.
		this.registerDomEvent(document, 'click', (evt: MouseEvent) => {
			console.log('click', evt);
		});

		// When registering intervals, this function will automatically clear the interval when the plugin is disabled.
		this.registerInterval(window.setInterval(() => console.log('setInterval'), 5 * 60 * 1000));
	}

	async activateRightPanel() {
		// 이미 ArchiFlow가 열려 있으면 재생성하지 않고 해당 리프를 활성화
		const existing = this.app.workspace.getLeavesOfType(VIEW_TYPE_ARCHIFLOW)
		if (existing.length > 0) {
			this.app.workspace.revealLeaf(existing[0])
			return
		}

		// 기존 우측 패널 리프를 가져와 그 자리를 대체. 없으면 새로 생성
		let rightLeaf = this.app.workspace.getRightLeaf(false)
		if (!rightLeaf) rightLeaf = this.app.workspace.getRightLeaf(true)
		if (!rightLeaf) {
			new Notice('fail to open right panel.')
			return
		}

		await rightLeaf.setViewState({ type: VIEW_TYPE_ARCHIFLOW, active: true })
		this.app.workspace.revealLeaf(rightLeaf)
	}

	onunload() {
		this.app.workspace.getLeavesOfType(VIEW_TYPE_ARCHIFLOW).forEach((leaf) => {
			leaf.detach();
		});
	}

	async loadSettings() {
		this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
	}

	async saveSettings() {
		await this.saveData(this.settings);
	}

}
