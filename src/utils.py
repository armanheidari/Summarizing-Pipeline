import os

class Utility:
    """
    A utility class for file-related operations.

    Methods:
        get_file_name: Extracts the file name without the extension.
        get_file_format: Extracts the file extension.
    """
    
    @classmethod
    def get_file_name(cls, file_path: str):
        """
        Extracts the file name without the extension.

        Args:
            file_path (str): The full path to the file.

        Returns:
            str: The file name without the extension.
        """
        return os.path.splitext(os.path.basename(file_path))[0]
    
    @classmethod
    def get_file_format(self, file_path: str) -> str:
        """
        Extracts the file extension.

        Args:
            file_path (str): The full path to the file.

        Returns:
            str: The file extension (without the dot).
        """
        return os.path.splitext(os.path.basename(file_path))[1][1:]