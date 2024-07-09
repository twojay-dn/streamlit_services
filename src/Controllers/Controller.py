from src.Models import State

class BaseController:
    @classmethod
    def get_state(cls, key, default=None):
        return State.get(key, default)
    
    @classmethod
    def set_state(cls, key, value, overwrite=True):
        if overwrite is False and cls.get_state(key) is not None:
            return cls.get_state(key)
        State.set(key, value)

__all__ = [
    "BaseController"
]