import { App, PluginSettingTab, Setting, Notice } from 'obsidian';
import MyPlugin from '../main';

export default class SampleSettingTab extends PluginSettingTab {
	plugin: MyPlugin;

	constructor(app: App, plugin: MyPlugin) {
		super(app, plugin);
		this.plugin = plugin;
	}

	display(): void {
		const {containerEl} = this;

		containerEl.empty();

		// AI Provider 선택
		new Setting(containerEl)
			.setName('AI Provider')
			.setDesc('사용할 AI 서비스를 선택하세요')
			.addDropdown(dropdown => dropdown
				.addOption('perplexity', 'Perplexity')
				.addOption('openai', 'OpenAI')
				.addOption('anthropic', 'Anthropic (Claude)')
				.setValue(this.plugin.settings.selectedProvider)
				.onChange(async (value: 'perplexity' | 'openai' | 'anthropic') => {
					this.plugin.settings.selectedProvider = value;
					await this.plugin.saveSettings();
					this.display(); // 설정을 다시 렌더링하여 해당 API Key 필드만 표시
				}));

		// Perplexity API Key
		if (this.plugin.settings.selectedProvider === 'perplexity') {
			new Setting(containerEl)
				.setName('Perplexity API Key')
				.setDesc('Perplexity API 키를 입력하세요')
				.addText(text => {
					text.setPlaceholder('Enter your Perplexity API key')
						.setValue(this.plugin.settings.perplexityApiKey)
						.onChange(async (value: string) => {
							this.plugin.settings.perplexityApiKey = value;
							await this.plugin.saveSettings();
						});
					text.inputEl.setAttribute('type', 'password');
				})
				.addButton(button => {
					button.setButtonText('연결 확인')
						.setCta()
						.onClick(async () => {
							await this.testConnection('perplexity', this.plugin.settings.perplexityApiKey);
						});
				});
		}

		// OpenAI API Key
		if (this.plugin.settings.selectedProvider === 'openai') {
			new Setting(containerEl)
				.setName('OpenAI API Key')
				.setDesc('OpenAI API 키를 입력하세요')
				.addText(text => {
					text.setPlaceholder('Enter your OpenAI API key')
						.setValue(this.plugin.settings.openaiApiKey)
						.onChange(async (value: string) => {
							this.plugin.settings.openaiApiKey = value;
							await this.plugin.saveSettings();
						});
					text.inputEl.setAttribute('type', 'password');
				})
				.addButton(button => {
					button.setButtonText('연결 확인')
						.setCta()
						.onClick(async () => {
							await this.testConnection('openai', this.plugin.settings.openaiApiKey);
						});
				});
		}

		// Anthropic API Key
		if (this.plugin.settings.selectedProvider === 'anthropic') {
			new Setting(containerEl)
				.setName('Anthropic API Key')
				.setDesc('Anthropic (Claude) API 키를 입력하세요')
				.addText(text => {
					text.setPlaceholder('Enter your Anthropic API key')
						.setValue(this.plugin.settings.anthropicApiKey)
						.onChange(async (value: string) => {
							this.plugin.settings.anthropicApiKey = value;
							await this.plugin.saveSettings();
						});
					text.inputEl.setAttribute('type', 'password');
				})
				.addButton(button => {
					button.setButtonText('연결 확인')
						.setCta()
						.onClick(async () => {
							await this.testConnection('anthropic', this.plugin.settings.anthropicApiKey);
						});
				});
		}
	}

	/**
	 * API 연결 테스트
	 */
	private async testConnection(provider: string, apiKey: string): Promise<void> {
		if (!apiKey) {
			new Notice('API Key를 먼저 입력해주세요.');
			return;
		}

		new Notice('연결을 확인하고 있습니다...');

		try {
			const serverUrl = 'http://localhost:8000';
			const response = await fetch(`${serverUrl}/test-connection`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					provider: provider,
					api_key: apiKey
				})
			});

			if (!response.ok) {
				throw new Error(`HTTP ${response.status}: ${response.statusText}`);
			}

			const data = await response.json();
			
			if (data.success) {
				new Notice(`✅ ${data.message}`);
			} else {
				new Notice(`❌ ${data.message}`);
			}
		} catch (error) {
			if (error instanceof TypeError && error.message.includes('fetch')) {
				new Notice('❌ 백그라운드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.');
			} else {
				new Notice(`❌ 연결 테스트 실패: ${error.message}`);
			}
		}
	}
}
