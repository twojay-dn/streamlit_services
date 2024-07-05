import streamlit as st
from States import State
from Classes import Agent

def render():
    st.title("Chat")
    
    curriculum = State.get("curriculum")
    if curriculum is None:
        st.error("Curriculum is not set")
        return
    teacher_persona
    teacher = Agent("assistant", "학생의 질문에 답변을 제공하는 역할을 합니다.")
    student = Agent("user", "선생님의 질문에 답변을 제공하는 역할을 합니다.")

    if st.button("Start"):
        former_message = ""
        for _ in range(10):
            former_message = teacher.inference(former_message)
            st.write(former_message)
            former_message = student.inference(former_message)
            st.write(former_message)
    
    