import os

class Utility:
    @classmethod
    def get_file_name(cls, file_path: str):
        return os.path.splitext(os.path.basename(file_path))[0]
    
    @classmethod
    def get_file_format(self, file_path: str) -> str:
        return os.path.splitext(os.path.basename(file_path))[1][1:]