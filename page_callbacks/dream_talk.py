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

def init_memory(memory_key_in_state : str):
  if memory_key_in_state not in st.session_state:
    for k, v in st.session_state.items():
      if k != memory_key_in_state:
        del st.session_state[k]
    st.session_state[memory_key_in_state] = Memory()
  return st.session_state[memory_key_in_state]

def display_chat_history(memory : Memory):
  for message in memory.get():
    st.chat_message(message["role"]).write(message["content"])

def inference(prompt : str, memory : Memory):
  return llm_client.inference(prompt, memory)

import json, functools

def retry_on_invalid_response(max_tries=3):
  if max_tries <= 0:
    raise ValueError("max_tries must be greater than to 0")
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      tries = max_tries
      while tries >= 0:
        if tries == 0:
          st.error("응답 생성에 실패했습니다. 다시 시도해 주세요.")
          return None
        response = func(*args, **kwargs)
        if check_response_validation(response):
          response = response.replace("```json\n", "").replace("\n```", "")
          parsed = json.loads(response)
          parsed['is_end'] = parsed['is_end'].lower() == "true"
          return parsed
        tries -= 1
      return None
    return wrapper
  return decorator

def check_response_validation(response: str):
  try:
    parsed = response.replace("```json\n", "").replace("\n```", "")
    parsed = json.loads(parsed)
    print(parsed)
    if 'response' not in parsed or 'is_end' not in parsed:
      return False
    if not isinstance(parsed['response'], str):
      return False
    if parsed['is_end'].lower() == "false" or parsed['is_end'].lower() == "true":
      return False
    return True
  except:
    return False

@retry_on_invalid_response()
def call_to_inference(prompt : str, memory : Memory) -> str:
  return inference(prompt, memory)

def talk_dream(memory_key_in_state : str):
  memory = init_memory(memory_key_in_state)
  
  height = 700
  display_container = st.container(height=round(height * 0.85))
  input_container = st.container(height=round(height * 0.15))
  info_container = st.container(height=round(height * 0.15))

  _last_response = None

  with input_container:
    prompt = st.chat_input("Say something")
    if prompt:
      memory.add_user_message(prompt)
      _last_response = call_to_inference(prompt, memory)
      if _last_response is None:
        st.error("응답 생성에 실패했습니다. 다시 시도해 주세요.")
      else:
        memory.add_assistant_message(json.loads(_last_response))

  with display_container:
    display_chat_history(memory)

  with info_container:
    if _last_response is not None:
      st.write(_last_response)

tab_list = [
  "꿈 내용 이야기하기",
  "꿈 내용 정보 추출 및 요약",
  "꿈 이미지 생성"
]

def run(key : str):
  tab1, tab2, tab3 = st.tabs(tab_list)
  
  with tab1:
    talk_dream("dream_talk")
  with tab2:
    st.write("꿈 내용 정보 추출 및 요약")
  with tab3:
    st.write("꿈 이미지 생성")