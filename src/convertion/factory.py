import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import AudioFormat
from src.convertion.base import AudioConvertor, VideoToAudio
from src.convertion.registry import AudioConvertorRegistry, VideoToAudioRegistry


class AudioConvertorFactory:
    """
    Factory class for creating audio convertors.

    This class provides a method to create instances of audio convertors based on the
    specified audio format.

    Methods:
        create: Creates an audio convertor for the specified format.
    """
    
    @classmethod
    def create(cls, audio_format: AudioFormat) -> AudioConvertor:
        """
        Creates an audio convertor for the specified format.

        Args:
            audio_format (AudioFormat): The target audio format.

        Returns:
            AudioConvertor: An instance of the appropriate audio convertor.

        Raises:
            Exception: If the specified format is not supported.
        """
        
        try:
            convertor_cls = AudioConvertorRegistry.get_registered(audio_format.value)
        except Exception as e:
            raise e from None
        
        return convertor_cls()


class VideoToAudioFactory:
    """
    Factory class for creating video-to-audio convertors.

    This class provides a method to create instances of video-to-audio convertors based
    on the specified audio format.

    Methods:
        create: Creates a video-to-audio convertor for the specified format.
    """
    
    @classmethod
    def create(cls, audio_format: AudioFormat) -> VideoToAudio:
        """
        Creates a video-to-audio convertor for the specified format.

        Args:
            audio_format (AudioFormat): The target audio format.

        Returns:
            VideoToAudio: An instance of the appropriate video-to-audio convertor.

        Raises:
            Exception: If the specified format is not supported.
        """
        
        try:
            convertor_cls = VideoToAudioRegistry.get_registered(audio_format.value)
        except Exception as e:
            raise e from None
        
        return convertor_cls()
