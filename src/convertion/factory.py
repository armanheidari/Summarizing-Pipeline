import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.convertion.base import AudioConvertor, AudioFormat
from src.convertion.registry import AudioConvertorRegistry


class AudioConvertorFactory:
    @classmethod
    def create(cls, audio_format: AudioFormat) -> AudioConvertor:
        try:
            convertor_cls = AudioConvertorRegistry.get_registered(audio_format.value)
        except Exception as e:
            raise e from None
        
        return convertor_cls()
