from typing import List, Type, Any

class SummarizingPipeline:
    def __init__(self, steps: List[Type[Any]]) -> None:
        self.steps = steps
    
    def summarize(self, input: Type[Any]) -> str:
        result = input
        
        for step in self.steps:
            result = step.run(result)
        
        return result