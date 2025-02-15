import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import Prompt
from src.prompts.base import THEMATIC, PRIORITY

class PromptFactory:
    """
    Factory class for creating summarization prompts.

    This class provides a method to retrieve the appropriate prompt template based on the
    specified summarization type (e.g., thematic, priority).

    Methods:
        create: Returns the prompt template for the specified summarization type.
    """
    
    @classmethod
    def create(cls, prompt: Prompt) -> str:
        """
        Returns the prompt template for the specified summarization type.

        Args:
            prompt (Prompt): The type of summarization prompt (e.g., thematic, priority).

        Returns:
            str: The prompt template for the specified summarization type.

        Raises:
            ValueError: If the specified prompt type is not supported.
        """
        if prompt.value == "Thematic":
            return THEMATIC
        elif prompt.value == "Priority":
            return PRIORITY
        else:
            raise ValueError(f"There is no prompt named {prompt.value}")