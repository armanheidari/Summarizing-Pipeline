from typing import Dict, Type, Any


class SpeechToTextRegistry:
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(stt_cls: Type[Any]):
            cls._registry[key] = stt_cls
            return stt_cls
        return decorator

    @classmethod
    def get_registered(cls, key: str) -> Type[Any]:
        stt_cls = cls._registry.get(key)
        if not stt_cls:
            raise ValueError(f"SpeechToText '{key}' not found in registry.")
        return stt_cls