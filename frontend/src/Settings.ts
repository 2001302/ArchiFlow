export interface MyPluginSettings {
	perplexityApiKey: string;
	openaiApiKey: string;
	anthropicApiKey: string;
	selectedProvider: 'perplexity' | 'openai' | 'anthropic';
	autoStartBackend: boolean;
}

export const DEFAULT_SETTINGS: MyPluginSettings = {
	perplexityApiKey: '',
	openaiApiKey: '',
	anthropicApiKey: '',
	selectedProvider: 'perplexity',
	autoStartBackend: false
};
