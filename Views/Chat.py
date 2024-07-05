import streamlit as st
from States import State

def render():
    st.title("Chat")
    st.write("This is the chat view")
    st.write(State.get("check"))