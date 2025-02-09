import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import SummerizerConfig
from src.summarization.base import Summarizer

class SummarizerFactory:
    @classmethod
    def create(cls, config: SummerizerConfig) -> Summarizer:
        return Summarizer(config)