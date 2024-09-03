import streamlit as st
from classes import Data
from enums import LLM_MODEL, LLM_VENDOR

def generate_config_interface(llm_vendor: LLM_VENDOR = None):
  parameter_package = {}
  for parameter in llm_vendor.get_needed_parameters():
    if parameter == "temperature":
      parameter_package[parameter] = st.slider(parameter, min_value=0.0, max_value=1.0, value=0.5)
    elif parameter == "max_tokens":
      parameter_package[parameter] = st.slider(parameter, min_value=1, max_value=4096, value=1024)
    elif parameter == "top_p":
      parameter_package[parameter] = st.slider(parameter, min_value=0.0, max_value=1.0, value=1.0)
    elif parameter == "frequency_penalty":
      parameter_package[parameter] = st.slider(parameter, min_value=-2.0, max_value=2.0, value=0.0)
    elif parameter == "presence_penalty":
      parameter_package[parameter] = st.slider(parameter, min_value=-2.0, max_value=2.0, value=0.0)
  return {**parameter_package}

def config_impl():
  st.write("설정")
  model_name = st.selectbox("모델 선택", [model.model_name for model in LLM_MODEL.get_model_list()])
  model_id = LLM_MODEL.get_model_id(model_name)
  vendor_type = LLM_MODEL.get_vendor(model_name)
  return {
    **generate_config_interface(vendor_type),
    "model_name": model_name,
    "model_id": model_id
  }

page_height = 1200

def hint_impl():
  st.write("힌트 생성")
  input_container = st.container(height=int(page_height * 0.2))

  with input_container:
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
      target_word = st.text_input("타겟 단어")
      target_word_category = st.text_input("타겟 단어 카테고리")
    with col2:
      space = st.container(border=False, height=20) # 버튼 위 공백
      random_hint_creation_button = st.button("랜덤 힌트 생성")
      custom_hint_creation_button = st.button("커스텀 힌트 생성")

  subcol1, subcol2 = st.columns([0.7, 0.3])
  with subcol1:
    generated_hint_list_container = st.container(height=int(page_height * 0.8))
    with generated_hint_list_container:
      generated_hint_list_display_position = st.empty()
  with subcol2:
    calculated_hint_list_container = st.container(height=int(page_height * 0.8))
    with calculated_hint_list_container:
      calculated_hint_list_display_position = st.empty()

  return {
    "target_word": target_word,
    "target_word_category": target_word_category,
    "random_hint_creation_button": random_hint_creation_button,
    "custom_hint_creation_button": custom_hint_creation_button,
    "generated_hint_list_container": generated_hint_list_container,
    "calculated_hint_list_container": calculated_hint_list_container,
    "generated_hint_list_display_position": generated_hint_list_display_position,
    "calculated_hint_list_display_position": calculated_hint_list_display_position
  }

def quiz_impl():
  col1, col2 = st.columns([0.8, 0.2])
  with col1:
    chat_history_container = st.container(height=int(page_height * 0.8))
    chat_input_container = st.container(height=int(100))
    with chat_history_container:
      for chat_message in st.session_state.chat_history:
        st.chat_message(chat_message)
    with chat_input_container:
      subcol1, subcol2 = st.columns([0.8, 0.2])
      with subcol1:
        chat_message = st.chat_input("user")
      with subcol2:
        submit_button = st.button("정답 제출")
  with col2:
    hint_display_container = st.container(height=int(page_height * 0.8))
    button_container = st.container(height=int(100))
    with hint_display_container:
      st.write("힌트")
      hint_display_position = st.empty()
    with button_container:
      subcol3, subcol4 = st.columns([0.5, 0.5])
      with subcol3:
        start_quiz_button = st.button("퀴즈 시작")
      with subcol4:
        reset_quiz_button = st.button("초기화")
  return {
    "start_quiz_button": start_quiz_button,
    "reset_quiz_button": reset_quiz_button,
    "hint_display_position": hint_display_position
  }

def interface_impl():
  st.title("Chatbot")
  tab1, tab2, tab3 = st.tabs(["설정", "힌트 생성", "퀴즈"])
  pocket = {}
  with tab1:
    pocket = {**pocket, **config_impl()}
  with tab2:
    pocket = {**pocket, **hint_impl()}
  with tab3:
    pocket = {**pocket, **quiz_impl()}
  return Data(pocket)

from utils import load_wordpool

class Interface:
  @staticmethod
  def run():
    return interface_impl()