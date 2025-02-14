import os
import io
import sys
import warnings
import subprocess
from enum import Enum
from abc import ABC, abstractmethod

from pydub import AudioSegment
from moviepy import VideoFileClip
from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import AudioFormat
from src.convertion.registry import AudioConvertorRegistry, VideoToAudioRegistry
from src.utils import Utility


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
    
    @abstractmethod
    def _convert(self) -> str:
        ...
    
    @abstractmethod
    def run(self, file_path: str) -> str:
        ...


@AudioConvertorRegistry.register(AudioFormat.WAV.value)
class AudioToWavConvertor(AudioConvertor):
    def _convert(self, audio: AudioSegment, file_name: str) -> str:
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
        
        return output_path
    
    def run(self, file_path: str) -> str:
        file_name = Utility.get_file_name(file_path)
        audio = self._validate_audio(file_path)
        
        return self._convert(audio, file_name)


class VideoToAudio(ABC):
    def __init__(self):
        ...
    
    def _validate_video(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError("The file does not exist!")
        try:
            video = VideoFileClip(file_path)
        except Exception as e:
            raise ValueError(f"The file is not a valid video file: {e}")

        video.close()
    
    @abstractmethod
    def _convert(self) -> str:
        ...
    
    @abstractmethod
    def run(self, file_path: str) -> str:
        ...


@VideoToAudioRegistry.register(AudioFormat.WAV.value)
class VideoToWavConvertor(VideoToAudio):
    def _convert(self, file_path: str, file_name: str) -> str:
        output_path = str(path_manager.get_base_directory() / f"audios/{file_name}.wav")
        
        ffmpeg_command = [
            "ffmpeg",
            "-i", file_path,
            "-ac", "1",
            "-ar", "16000",
            "-acodec", "pcm_s16le",
            output_path          
        ]
        
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"FFmpeg error: {stderr.decode()}")
        
        return output_path
    
    def run(self, file_path: str) -> str:
        file_name = Utility.get_file_name(file_path)
        self._validate_video(file_path)
        
        return self._convert(file_path, file_name)