import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import SummerizerConfig

class Summarizer:
    """A class for summarizing text using a language-specific prompt and a client API."""
    
    def __init__(self, config: SummerizerConfig):
        """
        Initialize the Summarizer.

        :param config: A `SummerizerConfig` dataclass containing the configuration for the summarizer.\n
            - `prompt`: The prompt for summarization.
            - `client`: The API client for making requests.
            - `model`: The model to use for summarization.
        """
        self.prompt = config.prompt
        self.client = config.client
        self.model = config.model
    
    def summarize(self, text: str) -> str:
        """
        Summarize the given text using the configured prompt and model.

        :param text: The text to summarize.
        :return str: The summarized text.
        """
        response = self.client.chat.completions.create(
            messages= [
                {
                    "role": "system", "content": self.prompt
                },
                {
                    "role": "user", "content": text
                }
            ],
            model=self.model,
            temperature=0
        )
        
        return response.choices[0].message.content
    