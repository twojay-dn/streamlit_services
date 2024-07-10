from src.Models import State
from src.utils import get_random_text, hash
from typing import Any

class BaseController:
    @classmethod
    def get_state(cls, key, default=None):
        return State.get(key, default)
    
    @classmethod
    def set_state(cls, key, value, overwrite=True):
        if overwrite is False and cls.get_state(key) is not None:
            return cls.get_state(key)
        State.set(key, value)

class TempController:
    def __init__(self, key : str = None):
        if key:
            self.key = hash(key)
        else:
            self.key = hash(get_random_text(10))
        State.set(self.key, {})
        
    def __del__(self):
        State.delete(self.key)
    
    def get(self, key : str, default : Any = None):
        return State.get(self.key).get(key, default)
    
    def set(self, key : str, value : Any, overwrite : bool = True):
        if overwrite is False and State.get(self.key)[key] is not None:
            return State.get(self.key)[key]
        State.get(self.key)[key] = value

__all__ = [
    "BaseController",
    "TempController"
]