from src.Views import Config, Generation_HQ, Quiz_v1, Quiz_v2

def route(choise: str):
    target_page = None
    match choise:
        case "Config":
            target_page = Config
        case "Generation_HQ":
            target_page = Generation_HQ
        case "Quiz_v1":
            target_page = Quiz_v1
        case "Quiz_v2":
            target_page = Quiz_v2
    target_page.page()