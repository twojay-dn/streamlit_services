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
        
    @classmethod
    def delete_state(cls, key : str or int):
        State.delete(key)
        
    @classmethod
    def create_temporary_storage(cls, key : str or int) -> str:
        if key:
            key = hash(key)
        else:
            key = hash(get_random_text(10))
        State.set(key, {})
        return key
    
    @classmethod
    def get_state_from_temporary_storage(cls, storage_key : str or int, key : str or int, default : Any = None) -> dict:
        return State.get(storage_key, {}).get(key, default)
    
    @classmethod
    def set_state_to_temporary_storage(cls, storage_key : str or int, key : str or int, value : Any, overwrite : bool = False):
        storage = State.get(storage_key, {})
        if overwrite is False and storage.get(key, None) is not None:
            return storage.get(key)
        storage[key] = value
        
    @classmethod
    def delete_temporary_storage(cls, key : str or int):
        State.delete(key)
        
class TempController:
    def __init__(self, key : str = None):
        self.key = self.get_random_key(key)
        State.set(self.key, {})
        
    def get_random_key(self, key : str = None):
        if key:
            result = hash(key)
        else:
            result = hash(get_random_text(10))
        return result

    def __del__(self):
        State.delete(self.key)
    
    def get(self, key : str or int, default : Any = None):
        storage : dict = State.get(self.key)
        if storage is None:
            return default
        return storage.get(key, default)
    
    def set(self, key : str or int, value : Any, overwrite : bool = False):
        storage : dict = State.get(self.key)
        if overwrite is False and storage.get(key, None) is not None:
            return storage.get(key)
        storage[key] = value

__all__ = [
    "BaseController",
    "TempController"
]