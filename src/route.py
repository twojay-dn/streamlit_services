from src.Views import Chat, Config

def route(choise: str):
    match choise:
        case "Chat":
            Chat.render()
        case "Config":
            Config.render()