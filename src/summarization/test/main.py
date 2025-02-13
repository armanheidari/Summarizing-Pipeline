import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.default import SUMMERIZER_CONFIG_DEFAULT
from src.summarization.factory import SummarizerFactory

if __name__ == "__main__":
    summerizer = SummarizerFactory.create(SUMMERIZER_CONFIG_DEFAULT)
    
    with open(str(path_manager.get_base_directory() / "transcriptions/like.txt"), mode="r", encoding="UTF-8") as f:
        text = f.read()
    
    with open("results.md", mode="w", encoding="UTF-8") as f:
        f.write(summerizer.summarize(text))