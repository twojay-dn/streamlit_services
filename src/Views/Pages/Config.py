import streamlit as st
from src.Views.Components import render_page

@render_page(name="Config")
def page():
    st.write("This is the config view")