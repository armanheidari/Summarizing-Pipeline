import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import AudioFormat
from src.convertion.factory import AudioConvertorFactory, VideoToAudioFactory

if __name__ == "__main__":
    convertor = AudioConvertorFactory.create(AudioFormat.WAV)
    
    convertor.convert(str(path_manager.get_base_directory() / r"samples\english.mp3"))
    
    convertor = VideoToAudioFactory.create(AudioFormat.WAV)
    
    convertor.convert(str(path_manager.get_base_directory() / r"samples\like.mp4"))