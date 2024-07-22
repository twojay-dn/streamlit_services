import streamlit as st
import os

from page_callbacks.dream_talk import run as dream_talk
from page_callbacks.dream_summary import run as dream_summary
from classes.llm import Memory

page_directory = f"{os.getcwd()}/pages"

pages = [
  st.Page(
    lambda :dream_talk(key="dream_talk"), 
    icon=":material/home:", 
    url_path="dream_talk", 
    title="Dream Talk"
  ),
  st.Page(
    lambda :dream_summary(key="dream_summary"), 
    icon=":material/settings:", 
    url_path="dream_summary", 
    title="Dream Summary"
  )
]

nav = st.navigation(pages, position="sidebar")
nav.run()