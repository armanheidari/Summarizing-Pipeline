from typing import List, Type, Any

class SummarizingPipeline:
    """
    A pipeline for summarizing input data through a series of processing steps.

    This class encapsulates a sequence of steps that process input data and produce a summarized output.
    Each step in the pipeline is expected to have a `run` method that takes input and returns processed output.

    Attributes:
        steps (List[Type[Any]]): A list of processing steps to execute in sequence.

    Methods:
        summarize: Executes the pipeline steps on the input data and returns the summarized result.
    """
    
    def __init__(self, steps: List[Type[Any]]) -> None:
        """
        Initializes the SummarizingPipeline with a list of processing steps.

        Args:
            steps (List[Type[Any]]): A list of processing steps to execute in sequence.
        """
        self.steps = steps
    
    def summarize(self, input: Type[Any]) -> str:
        """
        Executes the pipeline steps on the input data and returns the summarized result.

        Args:
            input (Type[Any]): The input data to process.

        Returns:
            str: The summarized output after processing through all pipeline steps.
        """
        result = input
        
        for step in self.steps:
            result = step.run(result)
        
        return result