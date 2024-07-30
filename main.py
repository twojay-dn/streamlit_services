import streamlit as st
import os

from page_callbacks.route import run

page_directory = f"{os.getcwd()}/page_callbacks/route"

pages = [
  st.Page(
    lambda : run(key="dream_talk"), 
    icon=":material/home:", 
    url_path="dream_talk", 
    title="Dream Talk"
  ),
]

nav = st.navigation(pages, position="sidebar")
nav.run()