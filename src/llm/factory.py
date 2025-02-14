import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import Client

class LLMFactory:
    @classmethod
    def create(cls, client: Client):
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