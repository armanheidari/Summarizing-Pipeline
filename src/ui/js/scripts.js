document.addEventListener('DOMContentLoaded', () => {
	const dragDropArea = document.getElementById('drag-drop-area');
	const fileUpload = document.getElementById('file-upload');
	const textInput = document.getElementById('text-input');
	const toggleConfigButton = document.getElementById('toggle-config');
	const configOptions = document.getElementById('config-options');
	const summarizeButton = document.getElementById('summarize-button');
	const resultsSection = document.getElementById('results-section');
	const resultsContent = document.getElementById('results-content');
	const copyResultsButton = document.getElementById('copy-results');
	const downloadResultsButton = document.getElementById('download-results');
	const clientDropdown = document.getElementById('client');
	const modelDropdown = document.getElementById('model');

	const clientModels = {
		OpenRouter: ['google/gemini-2.0-pro-exp-02-05:free'],
		Together: ['meta-llama/Llama-3.3-70B-Instruct-Turbo'],
	};

	let uploadedFile = null;
	let pastedText = '';
	let rawMarkdownContent = '';

	const populateModels = selectedClient => {
		const models = clientModels[selectedClient] || [];
		modelDropdown.innerHTML = '';
		models.forEach(model => {
			const option = document.createElement('option');
			option.value = model;
			option.textContent = model;
			modelDropdown.appendChild(option);
		});
	};

	populateModels(clientDropdown.value);

	clientDropdown.addEventListener('change', () => {
		const selectedClient = clientDropdown.value;
		populateModels(selectedClient);
	});

	fileUpload.addEventListener('change', e => {
		uploadedFile = e.target.files[0];
		dragDropArea.innerHTML = `<p>File ready: ${uploadedFile.name}</p>`;
	});

	dragDropArea.addEventListener('dragover', e => {
		e.preventDefault();
		dragDropArea.style.backgroundColor = '#3a3a50';
	});

	dragDropArea.addEventListener('dragleave', () => {
		dragDropArea.style.backgroundColor = '#34344a';
	});

	dragDropArea.addEventListener('drop', e => {
		e.preventDefault();
		dragDropArea.style.backgroundColor = '#34344a';
		uploadedFile = e.dataTransfer.files[0];
		dragDropArea.innerHTML = `<p>File ready: ${uploadedFile.name}</p>`;
	});

	textInput.addEventListener('input', () => {
		pastedText = textInput.value;
	});

	toggleConfigButton.addEventListener('click', () => {
		configOptions.classList.toggle('hidden');
	});

	summarizeButton.addEventListener('click', async () => {
		if (!uploadedFile && !pastedText) {
			alert('Please upload a file or paste some text.');
			return;
		}

		summarizeButton.textContent = 'Processing...';
		summarizeButton.disabled = true;

		const formData = new FormData();
		if (uploadedFile) {
			formData.append('file', uploadedFile);
		} else {
			formData.append('text', pastedText);
		}

		const language = document.getElementById('language').value;
		const audioFormat = document.getElementById('audio-format').value;
		const prompt = document.getElementById('prompt').value;
		const client = document.getElementById('client').value;
		const model = document.getElementById('model').value;

		formData.append('language', language);
		formData.append('audio_format', audioFormat);
		formData.append('prompt', prompt);
		formData.append('client', client);
		formData.append('model', model);

		try {
			const response = await fetch('http://localhost:8000/summarize', {
				method: 'POST',
				body: formData,
			});

			if (!response.ok) {
				throw new Error('Summarization failed');
			}

			const result = await response.json();

			rawMarkdownContent = result.summary;

			resultsContent.innerHTML = marked.parse(rawMarkdownContent);
			resultsSection.classList.remove('hidden');

			uploadedFile = null;
			fileUpload.value = '';
			dragDropArea.innerHTML = `<p>Drag & drop your file here</p><p>Or</p><label for="file-upload" id="file-upload-label">Choose a file</label><input type="file" id="file-upload" accept=".mp4,.mkv,.avi,.mov,.wav,.mp3,.ogg,.flac,.txt,.md"><p>Supports: Any video, audio, or text file</p>`;
			textInput.value = '';
			pastedText = '';
		} catch (error) {
			console.error('Error:', error);
			alert('An error occurred during summarization.');
		} finally {
			summarizeButton.textContent = 'Summarize';
			summarizeButton.disabled = false;
		}
	});

	copyResultsButton.addEventListener('click', () => {
		navigator.clipboard
			.writeText(rawMarkdownContent)
			.then(() => alert('Results copied to clipboard!'))
			.catch(() => alert('Failed to copy results.'));
	});

	downloadResultsButton.addEventListener('click', async () => {
		try {
			const suggestedFileName = uploadedFile
				? uploadedFile.name.replace(/\.[^/.]+$/, '.md')
				: 'summary.md';
			const fileHandle = await window.showSaveFilePicker({
				suggestedName: suggestedFileName,
				types: [
					{
						description: 'Markdown Files',
						accept: { 'text/markdown': ['.md'] },
					},
				],
			});

			const writableStream = await fileHandle.createWritable();
			await writableStream.write(rawMarkdownContent);
			await writableStream.close();

			alert('File saved successfully!');
		} catch (error) {
			console.error('Error saving file:', error);
			alert('Failed to save file.');
		}
	});
});
