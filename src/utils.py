import os, json, csv, hashlib, random, string
from typing import List
import streamlit as st

implemented_prompt_list = [
	"hints_generation_prompt",
	"questions_generation_prompt",
	"system_Quiz_type_00"
]

resources_directory = f"{os.getcwd()}/resource"
prompts_directory = f"{resources_directory}/prompts"

def hash(text : str, length : int = 10) -> str:
	return (hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)[:length]

def get_random_text(length : int) -> str:
	return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

controller = {
	"RUN_ENV" : "production"
}

from dotenv import load_dotenv
load_dotenv()
def get_api_key() -> str:
	# runtime_env = controller.get("RUN_ENV")
	# match runtime_env:
	# 	case "local":
	# 		api_key = os.getenv("OPENAI_API_KEY")
	# 	case "production":
	# 		api_key = st.secrets["OPENAI_API_KEY"]
	# 	case _:
	# 		raise ValueError("RUN_ENV must be 'local' or 'production' to use OpenAI")
	# return api_key
	return st.secrets["OPENAI_API_KEY"]

def get_prompt_path(prompt_name : str) -> str:
	assert prompt_name in implemented_prompt_list, f"Invalid prompt name : {prompt_name}"
	return f"{prompts_directory}/{prompt_name}.md"

def load_file(path : str) -> str:
	with open(path, "r", encoding="utf-8") as file:
		return file.read()

def load_json(path : str) -> dict:
	with open(path, "r", encoding="utf-8") as file:
		return json.load(file)
    
def load_prompt_from_name(prompt_name : str) -> str:
	return load_file(get_prompt_path(prompt_name))

def load_default_config_json() -> dict:
    return load_json(f"{resources_directory}/config.json")

def load_words() -> List[str]:
    result = []
    with open(f"{resources_directory}/words.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row)
    return result

import inspect

def validate_function_params(required : List[str] = []):
	def decorator(func):
		def wrapper(*args, **kwargs):
			inference_callback = args[1]  # 첫 번째 인자는 self, 두 번째 인자가 inference_callback
			sig = inspect.signature(inference_callback)
			for param in required:
				if param not in sig.parameters:
					raise ValueError(f"inference_callback must have a '{param}' parameter")
			return func(*args, **kwargs)
		return wrapper
	return decorator

__all__ = [
	"hash",
	"get_random_text",
	"load_prompt_from_name",
	"load_default_config_json",
	"load_words",
	"validate_function_params"
]