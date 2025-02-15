import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import Client

class LLMFactory:
    """
    Factory class for creating LLM (Large Language Model) configurations.

    This class provides a method to retrieve a list of supported models for a given LLM client.

    Methods:
        create: Returns a list of models supported by the specified client.
    """
    
    @classmethod
    def create(cls, client: Client):
        """
        Returns a list of models supported by the specified client.

        Args:
            client (Client): The LLM client (e.g., Together, OpenRouter).

        Returns:
            List[str]: A list of model names supported by the client.

        Raises:
            ValueError: If the specified client is not supported.
        """
        if client.value == "Together":
            return [
                "meta-llama/Llama-3.3-70B-Instruct-Turbo"
            ]
        elif client.value == "OpenRouter":
            return [
                "google/gemini-2.0-pro-exp-02-05:free"
            ]
        else:
            raise ValueError(f"There is no client named {client.value}")