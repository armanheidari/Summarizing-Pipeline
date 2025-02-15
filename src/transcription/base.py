import os
import sys
import wave
import json
import warnings
from enum import Enum
from abc import ABC, abstractmethod

from typing import Type, Any
from vosk import KaldiRecognizer


from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.utils import Utility
from src.config.config import Provider
from src.transcription.registry import SpeechToTextRegistry
from src.transcription.strategy import SpeechToTextStrategy, VoskStrategy


class SpeechToText(ABC):
    """
    Abstract base class for speech-to-text transcription.

    This class provides a template for transcribing audio files into text. Subclasses must
    implement the `_get_strategy` and `run` methods.

    Attributes:
        model: The speech recognition model to use for transcription.

    Methods:
        _get_strategy: Returns the strategy class for loading the speech recognition model.
        _validate_audio: Validates the input audio file.
        run: Transcribes the audio file into text (to be implemented by subclasses).
    """
    
    @classmethod
    @abstractmethod
    def _get_strategy(cls) -> SpeechToTextStrategy:
        """
        Returns the strategy class for loading the speech recognition model.

        Returns:
            SpeechToTextStrategy: The strategy class for loading the model.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("_get_strategy() is not implemented!")
    
    def __init__(self, model: Type[Any]):
        """
        Initializes the SpeechToText class with the provided model.

        Args:
            model: The speech recognition model to use for transcription.
        """
        self.model = model
    
    def _validate_audio(self, file_path: str) -> wave.Wave_read:
        """
        Validates the input audio file.

        Args:
            file_path (str): Path to the audio file.

        Returns:
            wave.Wave_read: The validated audio file object.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a valid WAV file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("The audio file does not exist!")
        elif Utility.get_file_format(file_path) != "wav":
            raise ValueError(f"The audio file is not a .wav audio!")
        
        wave_file = wave.open(file_path, "rb")
        
        if wave_file.getnchannels() != 1:
            warnings.warn("The audio file is not mono. Transcription accuracy may be affected.", UserWarning)
    
        if wave_file.getsampwidth() != 2:
            warnings.warn(f"The audio file is not 16-bit. Transcription accuracy may be affected.", UserWarning)
        
        if wave_file.getframerate() not in [8000, 16000]:
            warnings.warn(f"The audio file sample rate is not 8000 Hz or 16000 Hz. ({wave_file.getframerate()}) Transcription accuracy may be affected.", UserWarning)

        return wave_file
    
    @abstractmethod
    def run(self):
        """
        Transcribes the audio file into text.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("transcribe() is not implemented!")


@SpeechToTextRegistry.register(Provider.VOSK.value)
class VoskTranscriber(SpeechToText):
    """
    A speech-to-text transcriber using the Vosk library.

    This class implements the `SpeechToText` interface for transcribing audio files using
    the Vosk speech recognition model.

    Methods:
        _get_strategy: Returns the Vosk strategy class.
        _transcribe: Transcribes the audio file into text using the Vosk model.
        run: Executes the transcription process.
    """
    
    @classmethod
    def _get_strategy(cls):
        """
        Returns the Vosk strategy class.

        Returns:
            VoskStrategy: The strategy class for loading the Vosk model.
        """
        return VoskStrategy
    
    def _transcribe(self, wave_file: wave.Wave_read, file_name: str) -> str:
        """
        Transcribes the audio file into text using the Vosk model.

        Args:
            wave_file (wave.Wave_read): The validated audio file object.
            file_name (str): The name of the output transcription file.

        Returns:
            str: The transcribed text.
        """
        rec = KaldiRecognizer(self.model, wave_file.getframerate())
        transcription = []
        
        while True:
            data = wave_file.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                transcription.append(res.get("text", ""))
        
        final_res = json.loads(rec.FinalResult())
        transcription.append(final_res.get("text", ""))
        
        wave_file.close()
        transcription = " ".join(transcription)
        output_path = str(path_manager.get_base_directory() / f"transcriptions/{file_name}.txt")
        
        with open(output_path, mode="w", encoding="UTF-8") as f:
            f.write(transcription)
        
        return transcription
    
    def run(self, file_path: str) -> str:
        """
        Executes the transcription process.

        Args:
            file_path (str): Path to the input audio file.

        Returns:
            str: The transcribed text.
        """
        file_name = Utility.get_file_name(file_path)
        wave_file = self._validate_audio(file_path)
        
        return self._transcribe(wave_file, file_name)