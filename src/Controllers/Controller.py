from src.Models import State

class BaseController:
    @classmethod
    def get_state(cls, key, default=None):
        return State.get(key, default)
    
    @classmethod
    def set_state(cls, key, value):
        State.set(key, value)

__all__ = [
    "BaseController"
]