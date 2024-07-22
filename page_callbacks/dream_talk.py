import streamlit as st
from typing import Dict, Any
from classes.llm import Memory, Openai_LLM_Client
from utils import read_json, read_file
import os

@st.cache_data
def get_config(path : str=None) -> Dict[str, Any]:
  if path is None:
    path = f"{os.getcwd()}/model.config"
  return read_json(path)

@st.cache_data
def get_system_prompt(path : str=None):
  if path is None:
    path = f"{os.getcwd()}/resources/prompts/dream_dialogue.md"
  return read_file(path)

llm_client = Openai_LLM_Client(
  params=get_config(),
  system_prompt=get_system_prompt()
)

def display_chat_history(memory : Memory):
  for message in memory.get():
    st.chat_message(message["role"]).write(message["content"])

def inference(prompt : str, memory : Memory):
  return llm_client.inference(prompt, memory)

def call_to_inference(prompt : str, memory : Memory) -> str:
  memory.add_user_message(prompt)
  response = inference(prompt, memory)
  memory.add_assistant_message(response)
  return response

def run(key : str):
  if key not in st.session_state:
    for k, v in st.session_state.items():
      if k != key:
        del st.session_state[k]
    st.session_state[key] = Memory()
  display_chat_history(st.session_state[key])
  if prompt := st.chat_input("Say something"):
    st.chat_message("user").write(prompt)
    response = call_to_inference(prompt, st.session_state[key])
    st.chat_message("assistant").write(response)