import os
import sys
from enum import Enum
from abc import ABC, abstractmethod

from pydub import AudioSegment
from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.convertion.registry import AudioConvertorRegistry


class AudioFormat(Enum):
    WAV = "wav"


class AudioConvertor(ABC):
    def __init__(self):
        ...
    
    def _validate(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError("The file does not exists!")
        try:
            AudioSegment.from_file(file_path)
        except Exception as e:
            raise ValueError(f"The file is not a valid audio file: {e}")

        return file_path
    
    def _get_file_name(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def _get_file_format(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[1][1:]
    
    def _convert(self, file_path: str, new_file_path: str) -> None:
        base_format = self._get_file_format(file_path)
        converted_format = self._get_file_format(new_file_path)
        
        audio = AudioSegment.from_file(file_path, format=base_format)
        audio.export(new_file_path, format=converted_format)
    
    @abstractmethod
    def convert(self, file_path: str) -> None:
        ...

@AudioConvertorRegistry.register("wav")
class ToWavConvertor(AudioConvertor):
    def convert(self, file_path: str):
        self._validate(file_path)
        
        file_name = self._get_file_name(file_path)
        self._convert(file_path, str(path_manager.get_base_directory() / f"audios/{file_name}.wav"))

