from enum import Enum
from .Pages import Config, Generation, Quiz_type_00, Quiz_type_01, Quiz_type_02

class View_pages(Enum):
    Config = "Config"
    Quiz_type_00 = "Quiz_type_00"
    Quiz_type_01 = "Quiz_type_01"
    Quiz_type_02 = "Quiz_type_02"
    
    @staticmethod
    def get_view_list(retrieve_value: bool = False):
        if retrieve_value:
            return [view.value for view in View_pages]
        else:
            return [view for view in View_pages]

__all__ = [
    "View_pages",
    "Quiz_type_00",
    "Quiz_type_01",
    "Quiz_type_02",
    "Config",
    "Generation"
]