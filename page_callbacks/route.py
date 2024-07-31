import streamlit as st
from page_callbacks.phase_01 import talk_dream
from page_callbacks.phase_02 import dream_image
from page_callbacks.phase_03 import talk_with_picked_image
from page_callbacks.phase_04 import ask_mood


tab_list = [
  "꿈 내용 이야기하기",
  "꿈 이미지 생성",
  "선택한 이미지와 상호작용하기",
  "분위기 묻기"
]

def run(key : str):
  tab1, tab2, tab3, tab4 = st.tabs(tab_list)
  
  with tab1:
    talk_dream("dream_talk")
  with tab2:
    dream_image()
  with tab3:
    talk_with_picked_image()
  with tab4:
    ask_mood()