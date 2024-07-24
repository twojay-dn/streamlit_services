import streamlit as st
import os

from page_callbacks.dream_talk import run as dream_talk

page_directory = f"{os.getcwd()}/pages"

pages = [
  st.Page(
    lambda :dream_talk(key="dream_talk"), 
    icon=":material/home:", 
    url_path="dream_talk", 
    title="Dream Talk"
  ),
]

nav = st.navigation(pages, position="sidebar")
nav.run()