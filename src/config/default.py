import os
import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import (
    SummerizerConfig,
    PipelineConfig,
    Prompt,
    Client,
    AudioFormat,
    Language,
    Provider,
    PipelineType
)
from src.prompts.factory import PromptFactory
from src.clients.factory import ClientFactory
from src.llm.factory import LLMFactory

SUMMERIZER_CONFIG_DEFAULT = SummerizerConfig(
    prompt=PromptFactory.create(Prompt.THEMATIC_SUMMARIZER),
    client=ClientFactory.create(Client.OPENROUTER),
    model=LLMFactory.create(Client.OPENROUTER)[0]
)

PIPELINE_CONFIG_DEAFULT = PipelineConfig(
    summerizer_config=SUMMERIZER_CONFIG_DEFAULT,
    audio_format=AudioFormat.WAV,
    provider=Provider.VOSK,
    language=Language.ENGLISH,
    pipeline_type=PipelineType.TEXT
)