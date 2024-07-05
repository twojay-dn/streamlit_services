import streamlit as st
from States import State
from Views import Chat, TestGeneration

choosen = st.sidebar.selectbox("Select a view", ["Chat", "Test Generation"])
State.init({
    "check" : 42
})

if choosen == "Chat":
    Chat.render()
else:
    TestGeneration.render()