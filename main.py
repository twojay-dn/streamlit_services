import streamlit as st
from States import State
from Views import Chat, TestGeneration
from dotenv import load_dotenv

load_dotenv()
choosen = st.sidebar.selectbox("Select a view", ["Test Generation", "Chat"])
State.init({
    "check" : 42
})

if choosen == "Test Generation":
    TestGeneration.render()
elif choosen == "Chat":
    Chat.render()
else:
    st.error("잘못된 선택입니다.")
