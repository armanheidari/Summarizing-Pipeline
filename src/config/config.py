import sys
from dataclasses import dataclass

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.prompts.base import Prompt
from src.clients.base import Client

@dataclass
class SummerizerConfig:
    prompt: Prompt
    client: Client
    model: str