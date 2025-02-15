from typing import Dict, Type, Any


class AudioConvertorRegistry:
    """
    Registry for audio convertors.

    This class maintains a registry of audio convertor classes, allowing them to be
    dynamically retrieved based on a key (e.g., audio format).

    Attributes:
        _registry (Dict[str, Type[Any]]): A dictionary mapping keys to audio convertor classes.

    Methods:
        register: Registers an audio convertor class with a key.
        get_registered: Retrieves an audio convertor class by key.
    """
    
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, key: str):
        """
        Registers an audio convertor class with a key.

        Args:
            key (str): The key to associate with the convertor class.

        Returns:
            Callable: A decorator function for registering the convertor class.
        """
        def decorator(convertor_cls: Type[Any]):
            cls._registry[key] = convertor_cls
            return convertor_cls
        return decorator

    @classmethod
    def get_registered(cls, key: str) -> Type[Any]:
        """
        Retrieves an audio convertor class by key.

        Args:
            key (str): The key associated with the convertor class.

        Returns:
            Type[Any]: The registered convertor class.

        Raises:
            ValueError: If no convertor class is registered for the key.
        """
        convertor_cls = cls._registry.get(key)
        if not convertor_cls:
            raise ValueError(f"AudioConvertor '{key}' not found in registry.")
        return convertor_cls


class VideoToAudioRegistry:
    """
    Registry for video-to-audio convertors.

    This class maintains a registry of video-to-audio convertor classes, allowing them
    to be dynamically retrieved based on a key (e.g., audio format).

    Attributes:
        _registry (Dict[str, Type[Any]]): A dictionary mapping keys to video-to-audio convertor classes.

    Methods:
        register: Registers a video-to-audio convertor class with a key.
        get_registered: Retrieves a video-to-audio convertor class by key.
    """
    
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, key: str):
        """
        Registers a video-to-audio convertor class with a key.

        Args:
            key (str): The key to associate with the convertor class.

        Returns:
            Callable: A decorator function for registering the convertor class.
        """
        def decorator(convertor_cls: Type[Any]):
            cls._registry[key] = convertor_cls
            return convertor_cls
        return decorator

    @classmethod
    def get_registered(cls, key: str) -> Type[Any]:
        """
        Retrieves a video-to-audio convertor class by key.

        Args:
            key (str): The key associated with the convertor class.

        Returns:
            Type[Any]: The registered convertor class.

        Raises:
            ValueError: If no convertor class is registered for the key.
        """
        convertor_cls = cls._registry.get(key)
        if not convertor_cls:
            raise ValueError(f"VideoToAudio '{key}' not found in registry.")
        return convertor_cls