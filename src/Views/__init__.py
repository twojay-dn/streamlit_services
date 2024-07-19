from enum import Enum
from .Pages import Config, Generation_HQ, Quiz_v1, Quiz_v2

class View_pages(Enum):
    Config = "Config"
    Generation_HQ = "Generation_HQ"
    Quiz_v1 = "Quiz_v1"
    Quiz_v2 = "Quiz_v2"
        
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
    "Quiz_v1",
    "Quiz_v2"
]