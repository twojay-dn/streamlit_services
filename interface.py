import streamlit as st
from classes import Data
from enums import LLM_MODEL, LLM_VENDOR

def generate_config_interface(llm_vendor: LLM_VENDOR = None):
  st.write(llm_vendor.get_needed_parameters())
  parameter_package = {}
  for parameter in llm_vendor.get_needed_parameters():
    if parameter == "temperature":
      parameter_package[parameter] = st.slider(parameter, min_value=0.0, max_value=1.0, value=0.5)
    elif parameter == "max_tokens":
      parameter_package[parameter] = st.slider(parameter, min_value=1, max_value=4096, value=1024)
    elif parameter == "top_p":
      parameter_package[parameter] = st.slider(parameter, min_value=0.0, max_value=1.0, value=0.5)
    elif parameter == "frequency_penalty":
      parameter_package[parameter] = st.slider(parameter, min_value=-2.0, max_value=2.0, value=0.0)
    elif parameter == "presence_penalty":
      parameter_package[parameter] = st.slider(parameter, min_value=-2.0, max_value=2.0, value=0.0)
  return {**parameter_package}

def config_impl():
  st.write("설정")
  model_name = st.selectbox("모델 선택", [model.model_name for model in LLM_MODEL.get_model_list()])
  vendor_type = LLM_MODEL.get_vendor(model_name)
  return generate_config_interface(vendor_type)

def hint_impl():
  st.write("힌트 생성")
  return {"hint": "힌트"}

def quiz_impl():
  st.write("퀴즈")
  return {"quiz": "퀴즈"}

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

class Interface:
  st.set_page_config(layout="wide")

  @staticmethod
  def run():
    return interface_impl()