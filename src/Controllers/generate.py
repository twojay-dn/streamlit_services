from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

questions_generation_prompt_path = "./Prompts/questions_generation_prompt.txt"
hints_generation_prompt_path = "./Prompts/hints_generation_prompt.txt"
apikey = "sk-proj-1-20240307"

def generation_questions(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt = PromptTemplate.from_template(questions_generation_prompt_path)
    formatted_prompt = prompt.format(answer=answer, count=count)  # 수정된 부분
    llm = OpenAI(model=model_name, api_key=apikey)
    chain = formatted_prompt | llm  # 수정된 부분
    return chain.invoke({"answer": answer, "count": count})

def generation_hints(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt = PromptTemplate.from_template(hints_generation_prompt_path)
    formatted_prompt = prompt.format(answer=answer, count=count)  # 수정된 부분
    llm = OpenAI(model=model_name, api_key=apikey)
    chain = formatted_prompt | llm  # 수정된 부분
    return chain.invoke({"answer": answer, "count": count})

import os, json

implemented_prompt_list = [
    "hints_generation_prompt",
    "questions_generation_prompt"
]

prompts_directory = f"{os.getcwd()}/resources/prompts"
resources_directory = f"{os.getcwd()}/resources"

def get_prompt_path(prompt_name : str) -> str:
    assert prompt_name in implemented_prompt_list, f"Invalid prompt name : {prompt_name}"
    return f"{prompts_directory}/{prompt_name}.md"

def load_prompt(prompt_path : str) -> str:
    with open(prompt_path, "r") as file:
        return file.read()

def load_prompt_from_name(prompt_name : str) -> str:
    prompt_path = get_prompt_path(prompt_name)
    return load_prompt(prompt_path)

def load_default_config_json() -> dict:
    config_path = f"{resources_directory}/config.json"
    with open(config_path, "r") as file:
        return json.load(file)