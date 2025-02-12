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

from src.transcription.registry import SpeechToTextRegistry
from src.transcription.strategy import SpeechToTextStrategy, VoskStrategy

class Language(Enum):
    ENGLISH = "English"
    PERSIAN = "Persian"

class Provider(Enum):
    VOSK = "vosk"


class SpeechToText(ABC):
    @classmethod
    @abstractmethod
    def _get_strategy(cls) -> SpeechToTextStrategy:
        raise NotImplementedError("_get_strategy() is not implemented!")
    
    def __init__(self, model: Type[Any]):
        self.model = model
    
    def _validate_audio(self, file_path: str) -> wave.Wave_read:
        if not os.path.exists(file_path):
            raise FileNotFoundError("The audio file does not exist!")
        elif self._get_file_format(file_path) != "wav":
            raise ValueError(f"The audio file is not a .wav audio!")
        
        wave_file = wave.open(file_path, "rb")
        
        if wave_file.getnchannels() != 1:
            warnings.warn("The audio file is not mono. Transcription accuracy may be affected.", UserWarning)
    
        if wave_file.getsampwidth() != 2:
            warnings.warn(f"The audio file is not 16-bit. Transcription accuracy may be affected.", UserWarning)
        
        if wave_file.getframerate() not in [8000, 16000]:
            warnings.warn(f"The audio file sample rate is not 8000 Hz or 16000 Hz. ({wave_file.getframerate()}) Transcription accuracy may be affected.", UserWarning)

        return wave_file
    
    def _get_file_name(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def _get_file_format(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[1][1:]
    
    @abstractmethod
    def transcribe(self):
        raise NotImplementedError("transcribe() is not implemented!")


@SpeechToTextRegistry.register(Provider.VOSK.value)
class VoskTranscriber(SpeechToText):
    @classmethod
    def _get_strategy(cls):
        return VoskStrategy
    
    def _transcribe(self, wave_file: wave.Wave_read, file_name: str) -> str:
        
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
    
    def transcribe(self, file_path: str) -> str:
        file_name = self._get_file_name(file_path)
        wave_file = self._validate_audio(file_path)
        
        return self._transcribe(wave_file, file_name)