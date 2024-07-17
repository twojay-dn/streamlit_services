import os, json

def get_absolute_path(path : str) -> str:
	return os.path.abspath(path)

def read_file(path : str) -> str:
	with open(path, "r") as file:
		return file.read()

def read_json_file(path : str) -> dict:
	with open(path, "r") as file:
		return json.load(file)

import streamlit as st

def get_api_key(keyword : str) -> str:
	match keyword:
		case "openai-local":
			import dotenv
			dotenv.load_dotenv()
			return os.environ.get("OPENAI_API_KEY")
		case "openai-prod":
			return st.secrets.get("OPENAI_API_KEY")
		case _:
			raise ValueError(f"Invalid keyword: {keyword}")