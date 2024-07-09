from enum import Enum
from .Pages import Chat, Config, Generation

class View_pages(Enum):
    Chat = "Chat"
    Config = "Config"
    Generation = "Generation"
    
    @staticmethod
    def get_view_list(retrieve_value: bool = False):
        if retrieve_value:
            return [view.value for view in View_pages]
        else:
            return [view for view in View_pages]

__all__ = [
    "View_pages",
    "Chat",
    "Config",
    "Generation"
]