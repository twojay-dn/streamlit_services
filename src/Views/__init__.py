from enum import Enum
from .Pages import Config, Generation_HQ, Quiz

class View_pages(Enum):
    Config = "Config"
    Generation_HQ = "Generation_HQ"
    Quiz = "Quiz"
    
    @staticmethod
    def get_view_list(retrieve_value: bool = False):
        if retrieve_value:
            return [view.value for view in View_pages]
        else:
            return [view for view in View_pages]

__all__ = [
    "View_pages",
    "Config",
    "Generation_HQ",
    "Quiz"
]