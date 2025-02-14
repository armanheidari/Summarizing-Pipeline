import sys
from enum import Enum
from dataclasses import dataclass

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))


class Prompt(Enum):
    THEMATIC_SUMMARIZER = "Thematic"
    PRIORITY_SUMMARIZER = "Priority"


class Client(Enum):
    TOGETHER = "Together"
    OPENROUTER = "OpenRouter"


class AudioFormat(Enum):
    WAV = "wav"


class Language(Enum):
    ENGLISH = "English"
    PERSIAN = "Persian"


class Provider(Enum):
    VOSK = "vosk"


class PipelineType(Enum):
    VIDEO = "Video"
    AUDIO = "Audio"
    TEXT = "Text"


@dataclass
class SummerizerConfig:
    prompt: Prompt
    client: Client
    model: str


@dataclass
class PipelineConfig:
    summerizer_config: SummerizerConfig
    audio_format: AudioFormat
    provider: Provider
    language: Language
    pipeline_type: PipelineType 