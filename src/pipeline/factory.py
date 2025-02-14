import sys
from enum import Enum
from abc import ABC, abstractmethod

from path_handler import PathManager

path_manager = PathManager()
sys.path.append(str(path_manager.get_base_directory()))

from src.config.config import PipelineConfig
from src.convertion.factory import AudioConvertorFactory, VideoToAudioFactory
from src.transcription.factory import SpeechToTextFactory
from src.summarization.factory import SummarizerFactory
from src.pipeline.base import SummarizingPipeline


class SummarizingPipelineFactory:
    @classmethod
    def create(cls, pipeline_config: PipelineConfig) -> SummarizingPipeline:
        steps = []
        
        if pipeline_config.pipeline_type.value == "Video":
            steps.append(
                VideoToAudioFactory.create(pipeline_config.audio_format)
            )
            
            steps.append(
                SpeechToTextFactory.create(pipeline_config.provider, pipeline_config.language)
            )
        
        elif pipeline_config.pipeline_type.value == "Audio":
            steps.append(
                AudioConvertorFactory.create(pipeline_config.audio_format)
            )
        
            steps.append(
                SpeechToTextFactory.create(pipeline_config.provider, pipeline_config.language)
            )
        
        
        steps.append(
            SummarizerFactory.create(pipeline_config.summerizer_config)
        )
        
        return SummarizingPipeline(steps)