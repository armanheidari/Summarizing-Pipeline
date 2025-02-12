from vosk import Model as VoskModel
from path_handler import PathManager
from abc import ABC, abstractmethod

path_manager = PathManager()
base_directory = path_manager.get_base_directory()


class SpeechToTextStrategy(ABC):
    @classmethod
    @abstractmethod
    def load_model(self):
        ...


class VoskStrategy(SpeechToTextStrategy):
    _path_to_model = {
        "English": str(base_directory / "models/vosk-model-en-us-0.22"),
        "Persian": str(base_directory / "models/vosk-model-fa-0.42")
    }
    
    @classmethod
    def load_model(cls, language: str):
        model_path = cls._path_to_model.get(language)
        if not model_path:
            raise ValueError(f"The {language} Vosk model is not defined!")
        
        try:
            model = VoskModel(model_path)
        except Exception as e:
            raise e
        
        return model