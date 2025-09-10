export interface MyPluginSettings {
	mySetting: string;
	perplexityApiKey: string;
	openaiApiKey: string;
	anthropicApiKey: string;
	selectedProvider: 'perplexity' | 'openai' | 'anthropic';
}

export const DEFAULT_SETTINGS: MyPluginSettings = {
	mySetting: 'default',
	perplexityApiKey: '',
	openaiApiKey: '',
	anthropicApiKey: '',
	selectedProvider: 'perplexity'
};
