import { Editor, MarkdownView, Notice, Plugin, MarkdownPostProcessorContext, setIcon } from 'obsidian';
import { VIEW_TYPE_ARCHIFLOW } from './src/Constants';
import { MyPluginSettings, DEFAULT_SETTINGS } from './src/Settings';
import SidePannelView from './src/SidePannelView';
import SampleModal from './src/SampleModal';
import SampleSettingTab from './src/SampleSettingTab';
import { CodeBlockProcessor } from './src/CodeBlock';
import { BackendManager } from './src/BackendManager';

export default class MyPlugin extends Plugin {
	settings: MyPluginSettings;
	private codeBlockProcessor: CodeBlockProcessor;
	private backendManager: BackendManager;
	private healthCheckInterval: NodeJS.Timeout | null = null;

	async onload() {
		await this.loadSettings();

		// Initialize backend manager
		this.backendManager = new BackendManager((this.app.vault.adapter as any).basePath + '/.obsidian/plugins/arch-flow');

		// Initialize code block processor
		this.codeBlockProcessor = new CodeBlockProcessor(this.app);

		// Start backend server only if auto-start is enabled
		if (this.settings.autoStartBackend) {
			await this.startBackendServer();
		}

		// Start backend health check
		this.startBackendHealthCheck();

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
		const ribbonIconEl = this.addRibbonIcon('dice', 'Open ArchiFlow Panel', async (evt: MouseEvent) => {
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
		// Stop backend health check
		this.stopBackendHealthCheck();

		// Stop backend server
		this.stopBackendServer();

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

	/**
	 * Backend 서버 시작
	 */
	private async startBackendServer(): Promise<void> {
		try {
			// 이미 서버가 실행 중인지 확인
			if (await this.backendManager.isServerRunning()) {
				console.log('Backend 서버가 이미 실행 중입니다.');
				return;
			}

			// Backend 서버 시작
			const success = await this.backendManager.startBackend();
			if (!success) {
				console.warn('Backend 서버 시작에 실패했습니다.');
			}
		} catch (error) {
			console.error('Backend 서버 시작 중 오류:', error);
		}
	}

	/**
	 * Backend가 실행 중인지 확인하고 필요시 시작
	 */
	private async ensureBackendRunning(): Promise<boolean> {
		try {
			// 먼저 서버가 실제로 응답하는지 확인
			const isServerHealthy = await this.backendManager.isServerRunning();
			if (isServerHealthy) {
				console.log('Backend 서버가 정상적으로 실행 중입니다.');
				return true;
			}

			// 서버가 응답하지 않으면 프로세스 상태 확인
			if (this.backendManager.isBackendRunning()) {
				console.log('Backend 프로세스는 실행 중이지만 서버가 응답하지 않습니다. 재시작합니다...');
				await this.stopBackendServer();
				// 잠시 대기 후 재시작
				await new Promise(resolve => setTimeout(resolve, 2000));
			}

			// 실행 중이 아니라면 시작
			console.log('Backend 서버를 시작합니다...');
			await this.startBackendServer();
			
			// 시작 후 서버가 정상적으로 응답하는지 확인 (최대 3번 재시도)
			for (let attempt = 1; attempt <= 3; attempt++) {
				console.log(`서버 시작 확인 시도 ${attempt}/3...`);
				await new Promise(resolve => setTimeout(resolve, 2000)); // 2초 대기
				
				const isHealthy = await this.backendManager.isServerRunning();
				if (isHealthy) {
					console.log('Backend 서버가 성공적으로 시작되었습니다.');
					return true;
				}
				
				if (attempt < 3) {
					console.log(`시도 ${attempt} 실패. 재시작을 시도합니다...`);
					await this.stopBackendServer();
					await new Promise(resolve => setTimeout(resolve, 1000));
					await this.startBackendServer();
				}
			}
			
			console.error('Backend 서버 시작에 3번 모두 실패했습니다.');
			return false;
		} catch (error) {
			console.error('Backend 실행 확인 중 오류:', error);
			return false;
		}
	}

	/**
	 * Backend 서버 중지
	 */
	private async stopBackendServer(): Promise<void> {
		try {
			await this.backendManager.stopBackend();
		} catch (error) {
			console.error('Backend 서버 중지 중 오류:', error);
		}
	}

	/**
	 * BackendManager 인스턴스 반환
	 */
	getBackendManager(): BackendManager {
		return this.backendManager;
	}

	/**
	 * Backend 상태 모니터링 시작
	 */
	private startBackendHealthCheck(): void {
		// 30초마다 백엔드 상태 확인
		this.healthCheckInterval = setInterval(async () => {
			try {
				// auto-start가 비활성화된 경우 헬스 체크도 비활성화
				if (!this.settings.autoStartBackend) {
					return;
				}

				const isHealthy = await this.backendManager.isServerRunning();
				if (!isHealthy) {
					console.warn('Backend 서버가 응답하지 않습니다. 재시작을 시도합니다...');
					
					// 백엔드 프로세스가 실행 중이면 먼저 중지
					if (this.backendManager.isBackendRunning()) {
						await this.backendManager.stopBackend();
						// 중지 후 잠시 대기
						await new Promise(resolve => setTimeout(resolve, 2000));
					}
					
					// 재시작 시도
					await this.startBackendServer();
				}
			} catch (error) {
				console.error('헬스 체크 중 오류:', error);
			}
		}, 30000); // 30초마다 확인
	}

	/**
	 * Backend 상태 모니터링 중지
	 */
	private stopBackendHealthCheck(): void {
		if (this.healthCheckInterval) {
			clearInterval(this.healthCheckInterval);
			this.healthCheckInterval = null;
		}
	}

}
