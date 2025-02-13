import sys

from dotenv import load_dotenv
from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import Prompt
from src.prompts.base import THEMATIC, PRIORITY

load_dotenv(str(path_manager.get_base_directory() / ".env"))

class PromptFactory:
    @classmethod
    def create(cls, prompt: Prompt):
        if prompt.value == "Thematic":
            return THEMATIC
        elif prompt.value == "Priority":
            return PRIORITY
        else:
            raise ValueError(f"There is no prompt named {prompt.value}")