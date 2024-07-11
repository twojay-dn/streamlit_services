from src.Views import Config, Generation_HQ, Quiz

def route(choise: str):
    target_page = None
    match choise:
        case "Config":
            target_page = Config
        case "Generation_HQ":
            target_page = Generation_HQ
        case "Quiz":
            target_page = Quiz
    target_page.page()