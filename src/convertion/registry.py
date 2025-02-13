from typing import Dict, Type, Any


class AudioConvertorRegistry:
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(convertor_cls: Type[Any]):
            cls._registry[key] = convertor_cls
            return convertor_cls
        return decorator

    @classmethod
    def get_registered(cls, key: str) -> Type[Any]:
        convertor_cls = cls._registry.get(key)
        if not convertor_cls:
            raise ValueError(f"AudioConvertor '{key}' not found in registry.")
        return convertor_cls


class VideoToAudioRegistry:
    _registry: Dict[str, Type[Any]] = {}

    @classmethod
    def register(cls, key: str):
        def decorator(convertor_cls: Type[Any]):
            cls._registry[key] = convertor_cls
            return convertor_cls
        return decorator

    @classmethod
    def get_registered(cls, key: str) -> Type[Any]:
        convertor_cls = cls._registry.get(key)
        if not convertor_cls:
            raise ValueError(f"VideoToAudio '{key}' not found in registry.")
        return convertor_cls