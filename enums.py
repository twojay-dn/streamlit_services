from enum import Enum
import os

class Persona(Enum):
    범생이 = "a"
    궁금이 = "b"
    소심이 = "c"
    
def load_prompt_path(persona : Persona) -> str:
    return f"{os.getcwd()}/prompts/persona_student_{persona.value}.md"

def init_prompt(key : str) -> Persona:
    match key:
        case "범생이":
            return Persona.범생이
        case "궁금이":
            return Persona.궁금이
        case "소심이":
            return Persona.소심이
        case _:
            raise KeyError(f"Invalid key: {key}")