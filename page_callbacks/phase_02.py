
import streamlit as st

def dream_image():
  if st.session_state.get("dream_image") is None:
    st.error("꿈 이미지를 업로드해주세요.")
    return
  
  st.write("꿈 이미지 요약")