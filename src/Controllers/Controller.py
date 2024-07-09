from src.Models import State

class BaseController:
    @classmethod
    def get_state_by_key(cls, key):
        return State.get(key)
    
__all__ = [
    "BaseController"
]