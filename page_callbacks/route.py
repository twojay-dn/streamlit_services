import streamlit as st
from page_callbacks.phase_01 import talk_dream
from page_callbacks.phase_02 import dream_image


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