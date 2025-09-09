import { MarkdownPostProcessorContext } from 'obsidian';
import mermaid from 'mermaid';

export class CodeBlockProcessor {
	private app: any;

	constructor(app: any) {
		this.app = app;
	}

	async processArchFlowCodeBlock(source: string, el: HTMLElement, ctx: MarkdownPostProcessorContext) {
		// Create main container with clean design
		const container = el.createDiv({ cls: 'arch-flow-container' });
		container.style.border = '1px solid var(--background-modifier-border)';
		container.style.borderRadius = '8px';
		container.style.overflow = 'hidden';
		container.style.margin = '12px 0';
		container.style.backgroundColor = 'var(--background-primary)';

		// Create title input section
		const titleSection = container.createDiv({ cls: 'arch-flow-title-section' });
		titleSection.style.padding = '12px 16px';
		titleSection.style.borderBottom = '1px solid var(--background-modifier-border)';
		titleSection.style.backgroundColor = 'var(--background-secondary)';

		const titleInput = titleSection.createEl('input', { 
			type: 'text', 
			placeholder: 'enter diagram title...',
			cls: 'arch-flow-title-input'
		});
		titleInput.style.width = '100%';
		titleInput.style.padding = '8px 12px';
		titleInput.style.border = '1px solid var(--background-modifier-border)';
		titleInput.style.borderRadius = '6px';
		titleInput.style.backgroundColor = 'var(--background-primary)';
		titleInput.style.color = 'var(--text-normal)';
		titleInput.style.fontSize = '14px';
		titleInput.style.outline = 'none';
		titleInput.style.boxSizing = 'border-box';

		// Add focus styles
		titleInput.addEventListener('focus', () => {
			titleInput.style.borderColor = 'var(--interactive-accent)';
			titleInput.style.boxShadow = '0 0 0 2px var(--interactive-accent-2)';
		});

		titleInput.addEventListener('blur', () => {
			titleInput.style.borderColor = 'var(--background-modifier-border)';
			titleInput.style.boxShadow = 'none';
		});

		// Create mermaid diagram section
		const mermaidSection = container.createDiv({ cls: 'arch-flow-mermaid-section' });
		mermaidSection.style.padding = '20px';
		mermaidSection.style.textAlign = 'center';

		// Create a unique ID for this mermaid diagram
		const diagramId = `arch-flow-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
		const mermaidDiv = mermaidSection.createDiv({ cls: 'mermaid' });
		mermaidDiv.id = diagramId;
		mermaidDiv.textContent = source;

		// Initialize and render mermaid
		try {
			await mermaid.init(undefined, mermaidDiv);
		} catch (error) {
			console.error('Mermaid rendering error:', error);
			mermaidDiv.innerHTML = `<div style="color: var(--text-error); padding: 8px;">
				<strong>Mermaid 렌더링 오류:</strong><br>
				<pre style="background: var(--background-secondary); padding: 8px; border-radius: 4px; margin-top: 4px;"><code>${source}</code></pre>
			</div>`;
		}
	}

}
