import streamlit as st
from src.Controllers import BaseController
from src.Views.Components import render_page

@render_page(name="Chat")
def page():
    st.write(BaseController.get_state_by_key("check"))