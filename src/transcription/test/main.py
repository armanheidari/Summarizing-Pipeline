import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import Language, Provider
from src.transcription.factory import SpeechToTextFactory

if __name__ == "__main__":
    stt = SpeechToTextFactory.create(Provider.VOSK, Language.ENGLISH)
    
    stt.transcribe(str(path_manager.get_base_directory() / "audios\like.wav"))