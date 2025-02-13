import sys
from enum import Enum
from dataclasses import dataclass

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))


class Prompt(Enum):
    THEMATIC_SUMMARIZER = "Thematic"
    PRIORITY_SUMMARIZER = "Priority"


class AudioFormat(Enum):
    WAV = "wav"


class Client(Enum):
    TOGETHER = "Together"
    OPENROUTER = "OpenRouter"


class Language(Enum):
    ENGLISH = "English"
    PERSIAN = "Persian"


class Provider(Enum):
    VOSK = "vosk"


@dataclass
class SummerizerConfig:
    prompt: Prompt
    client: Client
    model: str