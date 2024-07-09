from src.Views import Chat, Config, Generation

def route(choise: str):
    target_page = None
    match choise:
        case "Generation":
            target_page = Generation
        case "Chat":
            target_page = Chat
        case "Config":
            target_page = Config
    target_page.page()