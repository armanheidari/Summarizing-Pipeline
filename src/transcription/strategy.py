from vosk import Model as VoskModel
from path_handler import PathManager
from abc import ABC, abstractmethod

path_manager = PathManager()
base_directory = path_manager.get_base_directory()


class SpeechToTextStrategy(ABC):
    """
    Abstract base class for speech-to-text strategies.

    This class provides a template for loading speech recognition models.

    Methods:
        load_model: Loads the speech recognition model (to be implemented by subclasses).
    """
    
    @classmethod
    @abstractmethod
    def load_model(self):
        """
        Loads the speech recognition model.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        ...


class VoskStrategy(SpeechToTextStrategy):
    """
    A strategy for loading Vosk speech recognition models.

    This class implements the `SpeechToTextStrategy` interface for loading Vosk models.

    Attributes:
        _path_to_model (Dict[str, str]): A dictionary mapping languages to their respective
                                         Vosk model paths.

    Methods:
        load_model: Loads the Vosk model for the specified language.
    """
    
    _path_to_model = {
        "English": str(base_directory / "models/vosk-model-en-us-0.22"),
        "Persian": str(base_directory / "models/vosk-model-fa-0.42")
    }
    
    @classmethod
    def load_model(cls, language: str):
        """
        Loads the Vosk model for the specified language.

        Args:
            language (str): The language of the model to load.

        Returns:
            VoskModel: The loaded Vosk model.

        Raises:
            ValueError: If the specified language is not supported.
            Exception: If the model fails to load.
        """
        model_path = cls._path_to_model.get(language)
        if not model_path:
            raise ValueError(f"The {language} Vosk model is not defined!")
        
        try:
            model = VoskModel(model_path)
        except Exception as e:
            raise e
        
        return model