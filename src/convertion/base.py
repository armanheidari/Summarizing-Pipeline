import os
import sys
import warnings
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
    
    def _validate_audio(self, file_path: str) -> AudioSegment:
        if not os.path.exists(file_path):
            raise FileNotFoundError("The file does not exist!")
        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            raise ValueError(f"The file is not a valid audio file: {e}")

        return audio
    
    def _get_file_name(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[0]
    
    def _get_file_format(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[1][1:]
    
    @abstractmethod
    def _convert(self) -> None:
        ...
    
    @abstractmethod
    def convert(self, file_path: str) -> None:
        ...

@AudioConvertorRegistry.register("wav")
class ToWavConvertor(AudioConvertor):
    def _convert(self, audio: AudioSegment, file_name: str) -> None:
        if audio.channels != 1:
            warnings.warn("The audio file is not mono. Converting to mono...", UserWarning)
            audio = audio.set_channels(1)
        
        if audio.sample_width != 2:
            warnings.warn("The audio file is not 16-bit. Converting to 16-bit...", UserWarning)
            audio = audio.set_sample_width(2)
        
        if audio.frame_rate not in [8000, 16000]:
            warnings.warn("The audio file sample rate is not 8000 Hz or 16000 Hz. Resampling to 16000 Hz...", UserWarning)
            audio = audio.set_frame_rate(16000)
        
        output_path = str(path_manager.get_base_directory() / f"audios/{file_name}.wav")
        audio.export(output_path, format="wav")
    
    def convert(self, file_path: str):
        file_name = self._get_file_name(file_path)
        audio = self._validate_audio(file_path)
        
        self._convert(audio, file_name)

