import sys
from enum import Enum
from dataclasses import dataclass

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))


class Prompt(Enum):
    """
    Enumeration for summarization prompt types.
    
    Attributes:
        THEMATIC_SUMMARIZER (str): Represents a thematic summarization prompt.
        PRIORITY_SUMMARIZER (str): Represents a priority-based summarization prompt.
    """
    THEMATIC_SUMMARIZER = "Thematic"
    PRIORITY_SUMMARIZER = "Priority"


class Client(Enum):
    """
    Enumeration for supported LLM clients.
    
    Attributes:
        TOGETHER (str): Represents the Together client.
        OPENROUTER (str): Represents the OpenRouter client.
    """
    TOGETHER = "Together"
    OPENROUTER = "OpenRouter"


class AudioFormat(Enum):
    """
    Enumeration for supported audio formats (related to VOSK).
    
    Attributes:
        WAV (str): Represents the WAV audio format.
    """
    WAV = "wav"


class Language(Enum):
    """
    Enumeration for supported languages.
    
    Attributes:
        ENGLISH (str): Represents the English language.
        PERSIAN (str): Represents the Persian language.
    """
    ENGLISH = "English"
    PERSIAN = "Persian"


class Provider(Enum):
    """
    Enumeration for supported transcription providers.
    
    Attributes:
        VOSK (str): Represents the Vosk transcription provider.
    """
    VOSK = "vosk"


class PipelineType(Enum):
    """
    Enumeration for pipeline types.
    
    Attributes:
        VIDEO (str): Represents a video processing pipeline.
        AUDIO (str): Represents an audio processing pipeline.
        TEXT (str): Represents a text processing pipeline.
    """
    VIDEO = "Video"
    AUDIO = "Audio"
    TEXT = "Text"


@dataclass
class SummerizerConfig:
    """
    Configuration class for the summarizer.

    Attributes:
        prompt (Prompt): The type of summarization prompt (e.g., thematic, priority).
        client (Client): The LLM client to use (e.g., OpenRouter, Together).
        model (str): The specific model to use for summarization.
    """
    prompt: Prompt
    client: Client
    model: str


@dataclass
class PipelineConfig:
    """
    Configuration class for the processing pipeline.

    Attributes:
        summerizer_config (SummerizerConfig): Configuration for the summarizer.
        audio_format (AudioFormat): The audio format to use for processing.
        provider (Provider): The transcription provider to use.
        language (Language): The language of the input data.
        pipeline_type (PipelineType): The type of pipeline (e.g., video, audio, text).
    """
    summerizer_config: SummerizerConfig
    audio_format: AudioFormat
    provider: Provider
    language: Language
    pipeline_type: PipelineType 