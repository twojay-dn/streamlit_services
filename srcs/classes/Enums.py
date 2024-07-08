from enum import Enum

class Views(Enum):
    CHAT = "Chat"
    TEST_GENERATION = "Test Generation"
    CONFIGURATION = "Configuration"

views_list_as_str = [view.value for view in Views]