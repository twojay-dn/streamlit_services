from src.Views import Config, Generation_HQ, Quiz, Quiz_H2H

def route(choise: str):
    target_page = None
    match choise:
        case "Config":
            target_page = Config
        case "Generation_HQ":
            target_page = Generation_HQ
        case "Quiz":
            target_page = Quiz
        case "Quiz_H2H":
            target_page = Quiz_H2H
    target_page.page()