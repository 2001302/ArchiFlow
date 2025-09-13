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

		// Backend 자동 시작 설정
		new Setting(containerEl)
			.setName('Backend 자동 시작')
			.setDesc('플러그인 로딩 시 백엔드 서버를 자동으로 시작합니다')
			.addToggle(toggle => toggle
				.setValue(this.plugin.settings.autoStartBackend)
				.onChange(async (value: boolean) => {
					this.plugin.settings.autoStartBackend = value;
					await this.plugin.saveSettings();
				}));

		// 구분선
		containerEl.createEl('hr');

		// config.json 파일 사용 안내
		new Setting(containerEl)
			.setName('AI 모델 설정')
			.setDesc('AI 모델 설정은 config.json 파일에서 관리됩니다. 플러그인 폴더의 config.json 파일을 편집하여 모델을 추가하세요.')
			.addButton(button => {
				button.setButtonText('config.json 열기')
					.setCta()
					.onClick(() => {
						// config.json 파일 열기
						const configPath = (this.plugin.app.vault.adapter as any).basePath + '/.obsidian/plugins/arch-flow/config.json';
						// 파일이 없으면 생성
						if (!this.plugin.app.vault.adapter.exists(configPath)) {
							const defaultConfig = {
								"name": "My Model",
								"version": "1.0.0",
								"models": [
									{
										"name": "GPT-4",
										"provider": "perplexity",
										"model": "gpt-4",
										"Authorization": "YOUR_API_KEY"
									}
								]
							};
							this.plugin.app.vault.adapter.write(configPath, JSON.stringify(defaultConfig, null, 2));
						}
						// 파일 열기
						this.app.workspace.openLinkText(configPath, '');
					});
			});
	}

}
