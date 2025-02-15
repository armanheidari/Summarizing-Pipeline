import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import Language, Provider
from src.transcription.base import SpeechToText
from src.transcription.registry import SpeechToTextRegistry

class SpeechToTextFactory:
    """
    Factory class for creating SpeechToText instances.

    This class provides a method to create a SpeechToText instance based on the specified
    provider and language.

    Methods:
        create: Creates a SpeechToText instance with the specified provider and language.
    """
    
    @classmethod
    def create(cls, provider: Provider, language: Language) -> SpeechToText:
        """
        Creates a SpeechToText instance with the specified provider and language.

        Args:
            provider (Provider): The speech-to-text provider (e.g., Vosk).
            language (Language): The language of the input audio.

        Returns:
            SpeechToText: An instance of the SpeechToText class configured with the
                          specified provider and language.

        Raises:
            Exception: If the provider or language is not supported.
        """
        try:
            stt_cls = SpeechToTextRegistry.get_registered(provider.value)
            strategy = stt_cls._get_strategy()
            model = strategy.load_model(language.value)
        except Exception as e:
            raise e from None
        
        return stt_cls(model)