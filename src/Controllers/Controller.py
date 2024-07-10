from src.Models import State
from src.utils import get_random_text, hash
from typing import Any

class BaseController:
    @classmethod
    def get_state(cls, key : str or int, default=None):
        return State.get(key, default)
    
    @classmethod
    def set_state(cls, key : str or int, value : Any, overwrite : bool = False):
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
    
    def get(self, key : str or int, default : Any = None):
        storage : dict = State.get(self.key)
        return storage.get(key, default)
    
    def set(self, key : str or int, value : Any, overwrite : bool = False):
        if overwrite is False and State.get(self.key)[key] is not None:
            return State.get(self.key)[key]
        storage : dict = State.get(self.key)
        storage[key] = value

__all__ = [
    "BaseController",
    "TempController"
]