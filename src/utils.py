import os, json, csv
from typing import List

implemented_prompt_list = [
    "hints_generation_prompt",
    "questions_generation_prompt"
]

resources_directory = f"{os.getcwd()}/resource"
prompts_directory = f"{resources_directory}/prompts"


def get_prompt_path(prompt_name : str) -> str:
    assert prompt_name in implemented_prompt_list, f"Invalid prompt name : {prompt_name}"
    return f"{prompts_directory}/{prompt_name}.md"

def load_file(path : str) -> str:
    with open(path, "r") as file:
        return file.read()

def load_json(path : str) -> dict:
    with open(path, "r") as file:
        return json.load(file)
    
def load_prompt_from_name(prompt_name : str) -> str:
    prompt_path = get_prompt_path(prompt_name)
    return load_file(prompt_path)

def load_default_config_json() -> dict:
    config_path = f"{resources_directory}/config.json"
    return load_json(config_path)

def load_words() -> List[str]:
    words_path = f"{resources_directory}/words.csv"
    result = []
    with open(words_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row)
    return result

__all__ = [
    "load_prompt_from_name",
    "load_default_config_json",
    "load_words"
]