from typing import Dict, Type, Any


class SpeechToTextRegistry:
    """
    Registry for speech-to-text providers.

    This class maintains a registry of speech-to-text provider classes, allowing them to be
    dynamically retrieved based on a key (e.g., provider name).

    Attributes:
        _registry (Dict[str, Type[Any]]): A dictionary mapping keys to speech-to-text provider classes.

    Methods:
        register: Registers a speech-to-text provider class with a key.
        get_registered: Retrieves a speech-to-text provider class by key.
    """
    
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, key: str):
        """
        Registers a speech-to-text provider class with a key.

        Args:
            key (str): The key to associate with the provider class.

        Returns:
            Callable: A decorator function for registering the provider class.
        """
        def decorator(stt_cls: Type[Any]):
            cls._registry[key] = stt_cls
            return stt_cls
        return decorator

    @classmethod
    def get_registered(cls, key: str) -> Type[Any]:
        """
        Retrieves a speech-to-text provider class by key.

        Args:
            key (str): The key associated with the provider class.

        Returns:
            Type[Any]: The registered provider class.

        Raises:
            ValueError: If no provider class is registered for the key.
        """
        stt_cls = cls._registry.get(key)
        if not stt_cls:
            raise ValueError(f"SpeechToText '{key}' not found in registry.")
        return stt_cls