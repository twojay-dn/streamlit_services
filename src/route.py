from src.Views import Config, Chat

def route(choise: str):
    match choise:
        case "Chat":
            Chat.render()
        case "Config":
            Config.render()