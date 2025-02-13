import os
import sys
from dotenv import load_dotenv

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import (
    SummerizerConfig,
    Prompt,
    Client
)
from src.prompts.factory import PromptFactory
from src.clients.factory import ClientFactory

load_dotenv(str(path_manager.get_base_directory() / ".env"))

SUMMERIZER_CONFIG_DEFAULT = SummerizerConfig(
    prompt=PromptFactory.create(Prompt.THEMATIC_SUMMARIZER),
    client=ClientFactory.create(Client.OPENROUTER),
    model="google/gemini-2.0-pro-exp-02-05:free",
)