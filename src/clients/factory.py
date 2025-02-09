import os
import sys

from dotenv import load_dotenv
from path_handler import PathManager
from together import Client as TogetherClient
from openai import OpenAI

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.clients.base import Client

load_dotenv(str(path_manager.get_base_directory() / ".env"))

class ClientFactory:
    @classmethod
    def create(cls, client: Client):
        if client.value == "Together":
            return TogetherClient.client(
                api_key=os.getenv("TOGETHER_TOKEN")
            )
        elif client.value == "OpenRouter":
            return OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_TOKEN"),
            )
        else:
            raise ValueError(f"There is no client named {client.value}")