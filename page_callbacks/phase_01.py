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

llm_client_phase_inform = Openai_LLM_Client(
  params=get_config(),
  system_prompt=get_system_prompt(f"{os.getcwd()}/resources/prompts/dream_dialogue_phase_inform.md")
)

llm_client_phase_summary = Openai_LLM_Client(
  params=get_config(),
  system_prompt=get_system_prompt(f"{os.getcwd()}/resources/prompts/dream_dialogue_phase_summary.md")
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

# call_to_inference의 경우 요청을 마치면 json 형식으로 응답이 나옴
# 이 응답이 유효한지 검증하는 데코레이터를 추가함, 유효하지 않으면 요청을 다시 보냄
# default 시도 횟수는 retry_on_invalid_response()에 매개변수 참조
# @retry_on_invalid_response()
# def call_to_inference(prompt : str, memory : Memory) -> str:
#   return inference(prompt, memory)
from classes.llm import Retrier, CONDITION_FORMAT, inference

def convert_isEnd_to_bool(parsed : Dict[str, Any]) -> Dict[str, Any]:
  parsed['is_end'] = parsed['is_end'].lower() == "true"
  return parsed

@Retrier.retry_on_invalid_response(
  max_tries=3,
  condition_format=CONDITION_FORMAT.JSON,
  post_processor=convert_isEnd_to_bool
)
def call_to_response_asking_dream(memory : Memory) -> str:
  return inference(llm_client_phase_inform, memory)

@Retrier.retry_on_invalid_response(
  max_tries=3,
  condition_format=CONDITION_FORMAT.JSON
)
def call_to_summary(memory : Memory) -> str:
  return inference(llm_client_phase_summary, memory)


from dream_lib.static_messages import greeting
import random
from shared import dream_image_key, dalle_drawing_style_code

def talk_dream(memory_key_in_state : str) -> None:
  memory = init_memory(memory_key_in_state)
  
  height = 500
  display_container = st.container(height=round(height * 1.2))
  input_container = st.container(height=round(height * 0.2))
  info_container = st.container(height=round(height * 0.5))

  _last_response = None
  if len(memory) == 0:
    memory.add_assistant_message(random.choice(greeting))

  with input_container:
    prompt = st.chat_input("Say something")
    if prompt:
      memory.add_user_message(prompt)
      _last_response = call_to_response_asking_dream(memory)
      print(_last_response)
      if _last_response is None:
        st.error("응답 생성에 실패했습니다. 다시 시도해 주세요.")
      else:
        memory.add_assistant_message(_last_response['response'])

  with display_container:
    display_chat_history(memory)
  
  with info_container:
    if _last_response and _last_response['is_end'] == True:
      st.success("꿈 내용 요약을 성공적으로 생성했습니다.")
      summary = call_to_summary(memory)
      st.session_state[dream_image_key] = summary
      st.write(summary)
    else:
      st.info("아직 꿈에 대한 정보를 생성하지 않았습니다.")