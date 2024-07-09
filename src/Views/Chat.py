import streamlit as st
from src.Controllers import BaseController

def render():
    st.title("Chat")
    st.write("This is the chat view")
    st.write(BaseController.get_state_by_key("check"))