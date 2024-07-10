from src.Views import Config, Quiz_type_00, Quiz_type_01, Quiz_type_02

def route(choise: str):
    target_page = None
    match choise:
        case "Config":
            target_page = Config
        case "Quiz_type_00":
            target_page = Quiz_type_00
        case "Quiz_type_01":
            target_page = Quiz_type_01
        case "Quiz_type_02":
            target_page = Quiz_type_02
    target_page.page()