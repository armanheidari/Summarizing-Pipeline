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
    """
    Abstract base class for audio conversion.

    This class provides a template for converting audio files to a specific format.
    Subclasses must implement the `_convert` and `run` methods.

    Methods:
        _validate_audio: Validates the input audio file.
        _convert: Converts the audio file (to be implemented by subclasses).
        run: Executes the conversion process (to be implemented by subclasses).
    """
    
    def __init__(self):
        """Initializes the audio convertor."""
        ...
    
    def _validate_audio(self, file_path: str) -> AudioSegment:
        """
        Validates the input audio file.

        Args:
            file_path (str): Path to the audio file.

        Returns:
            AudioSegment: The validated audio segment.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a valid audio file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("The file does not exist!")
        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e:
            raise ValueError(f"The file is not a valid audio file: {e}")

        return audio
    
    @abstractmethod
    def _convert(self) -> str:
        """
        Converts the audio file to the target format.

        Args:
            audio (AudioSegment): The audio segment to convert.
            file_name (str): The name of the output file.

        Returns:
            str: Path to the converted audio file.
        """
        ...
    
    @abstractmethod
    def run(self, file_path: str) -> str:
        """
        Executes the audio conversion process.

        Args:
            file_path (str): Path to the input audio file.

        Returns:
            str: Path to the converted audio file.
        """
        ...


@AudioConvertorRegistry.register(AudioFormat.WAV.value)
class AudioToWavConvertor(AudioConvertor):
    """
    Converts audio files to WAV format.

    This class handles the conversion of audio files to WAV format, ensuring the output
    meets specific requirements (mono, 16-bit, 16 kHz sample rate).

    Methods:
        _convert: Converts the audio file to WAV format.
        run: Executes the conversion process.
    """
    
    def _convert(self, audio: AudioSegment, file_name: str) -> str:
        """
        Converts the audio file to WAV format.

        Args:
            audio (AudioSegment): The audio segment to convert.
            file_name (str): The name of the output file.

        Returns:
            str: Path to the converted WAV file.
        """
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
        """
        Executes the audio-to-WAV conversion process.

        Args:
            file_path (str): Path to the input audio file.

        Returns:
            str: Path to the converted WAV file.
        """
        file_name = Utility.get_file_name(file_path)
        audio = self._validate_audio(file_path)
        
        return self._convert(audio, file_name)


class VideoToAudio(ABC):
    """
    Abstract base class for video-to-audio conversion.

    This class provides a template for extracting audio from video files.
    Subclasses must implement the `_convert` and `run` methods.

    Methods:
        _validate_video: Validates the input video file.
        _convert: Extracts audio from the video file (to be implemented by subclasses).
        run: Executes the conversion process (to be implemented by subclasses).
    """
    
    def __init__(self):
        """Initializes the video-to-audio convertor."""
        ...
    
    def _validate_video(self, file_path: str) -> None:
        """
        Validates the input video file.

        Args:
            file_path (str): Path to the video file.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a valid video file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("The file does not exist!")
        try:
            video = VideoFileClip(file_path)
        except Exception as e:
            raise ValueError(f"The file is not a valid video file: {e}")

        video.close()
    
    @abstractmethod
    def _convert(self, file_path: str, file_name: str) -> str:
        """
        Extracts audio from the video file.

        Args:
            file_path (str): Path to the input video file.
            file_name (str): Name of the output audio file.

        Returns:
            str: Path to the extracted audio file.
        """
        ...
    
    @abstractmethod
    def run(self, file_path: str) -> str:
        """
        Executes the video-to-audio conversion process.

        Args:
            file_path (str): Path to the input video file.

        Returns:
            str: Path to the extracted audio file.
        """
        ...


@VideoToAudioRegistry.register(AudioFormat.WAV.value)
class VideoToWavConvertor(VideoToAudio):
    """
    Extracts audio from video files and saves it in WAV format.

    This class uses FFmpeg to extract audio from video files and ensures the output
    meets specific requirements (mono, 16-bit, 16 kHz sample rate).

    Methods:
        _convert: Extracts audio from the video file and saves it as WAV.
        run: Executes the video-to-WAV conversion process.
    """
    
    def _convert(self, file_path: str, file_name: str) -> str:
        """
        Extracts audio from the video file and saves it as WAV.

        Args:
            file_path (str): Path to the input video file.
            file_name (str): Name of the output audio file.

        Returns:
            str: Path to the extracted WAV file.

        Raises:
            Exception: If FFmpeg encounters an error during the conversion.
        """
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
        """
        Executes the video-to-WAV conversion process.

        Args:
            file_path (str): Path to the input video file.

        Returns:
            str: Path to the extracted WAV file.
        """
        file_name = Utility.get_file_name(file_path)
        self._validate_video(file_path)
        
        return self._convert(file_path, file_name)