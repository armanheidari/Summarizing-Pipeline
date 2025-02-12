import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.transcription.base import SpeechToText, Language, Provider
from src.transcription.registry import SpeechToTextRegistry

class SpeechToTextFactory:
    @classmethod
    def create(cls, provider: Provider, language: Language) -> SpeechToText:
        try:
            stt_cls = SpeechToTextRegistry.get_registered(provider.value)
            strategy = stt_cls._get_strategy()
            model = strategy.load_model(language.value)
        except Exception as e:
            raise e from None
        
        return stt_cls(model)