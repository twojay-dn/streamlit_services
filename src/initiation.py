import streamlit as st
from .Chat.page import render_chat
import json

def preprocess():
  ...

def init():
  preprocess()
  config = json.load(open("resource/config.json", encoding="utf-8"))
  st.set_page_config(layout="wide")
  st.title("이미지 기반 튜터링 테스트")
  st.subheader(f"과목 : {config.get('class').get('name')}")
  render_chat()

__all__ = [
	"init"
]