import { App, PluginSettingTab, Setting } from 'obsidian';
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
				});
		}

		// 기존 설정
		new Setting(containerEl)
			.setName('Setting #1')
			.setDesc('It\'s a secret')
			.addText(text => text
				.setPlaceholder('Enter your secret')
				.setValue(this.plugin.settings.mySetting)
				.onChange(async (value) => {
					this.plugin.settings.mySetting = value;
					await this.plugin.saveSettings();
				}));
	}
}
