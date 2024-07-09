from src.Models import State

def init_state():
    State.set("check", 42)
    
__all__ = [
    "init_state"
]