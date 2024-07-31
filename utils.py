import json
import streamlit as st
from typing import Dict, Any
from page_callbacks.shared import resources_path, prompt_path

def read_file(file_path : str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_json(file_path : str) -> dict:
  with open(file_path, "r", encoding="utf-8") as file:
    return json.load(file)
  
def insert_parameters(prompt : str, parameters : dict) -> str:
  for key, value in parameters.items():
    prompt = prompt.replace(f"<{key}>", value)
  return prompt

@st.cache_data
def get_config(path : str=None) -> Dict[str, Any]:
  if path is None:
    path = f"{resources_path}/model.config"
  return read_json(path)

@st.cache_data
def get_system_prompt(path : str=None):
  if path is None:
    path = f"{resources_path}/prompts/dream_dialogue.md"
  return read_file(path)