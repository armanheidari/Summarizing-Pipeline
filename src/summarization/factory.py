import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import SummerizerConfig
from src.summarization.base import Summarizer

class SummarizerFactory:
    """
    Factory class for creating Summarizer instances.

    This class provides a method to create a Summarizer instance based on the provided configuration.

    Methods:
        create: Creates a Summarizer instance with the specified configuration.
    """
    
    @classmethod
    def create(cls, config: SummerizerConfig) -> Summarizer:
        """
        Creates a Summarizer instance with the specified configuration.

        Args:
            config (SummerizerConfig): The configuration for the summarizer, including the prompt, client, and model.

        Returns:
            Summarizer: An instance of the Summarizer class configured with the provided settings.
        """
        return Summarizer(config)