import streamlit as st
from States import State
from Views import Chat, TestGeneration
from enums import Persona, init_prompt

choosen = st.sidebar.selectbox("Select a view", ["Test Generation", "Chat"])
State.init({
    "check" : 42
})
choosen_persona = st.sidebar.selectbox("Select a persona", ["범생이", "궁금이", "소심이"])
State.set("persona", init_prompt(choosen_persona))

if choosen == "Test Generation":
    TestGeneration.render()
elif choosen == "Chat":
    Chat.render()
else:
    st.error("잘못된 선택입니다.")