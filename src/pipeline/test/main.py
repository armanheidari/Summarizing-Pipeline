import sys

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.default import PIPELINE_CONFIG_DEAFULT
from src.pipeline.factory import SummarizingPipelineFactory

if __name__ == "__main__":
    summerizer = SummarizingPipelineFactory.create(PIPELINE_CONFIG_DEAFULT)
    
    with open("results.md", mode="w", encoding="UTF-8") as f:
        f.write(
            summerizer.summarize(
                str(path_manager.get_base_directory() / r"samples\like.mp4")
            )
        )