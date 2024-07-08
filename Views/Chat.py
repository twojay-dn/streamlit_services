import streamlit as st
from States import State
from Classes import Agent
from utils import read_file
from enums import Persona, load_prompt_path

def compose_prompt(prompt : str, params : dict) -> str:
    if params is None:
        return prompt
    return prompt.format(**params)

def render():
    st.title("Chat")
    
    curriculum = State.get("curriculum")
    if curriculum is None:
        st.error("Curriculum is not set")
        return
    teacher_persona_params = {
        "grade" : State.get("grade"),
        "subject" : State.get("subject"),
        "unit" : State.get("unit"),
        "title" : State.get("title"),
        "content" : State.get("content"),
        "teaching_generated_prompt" : State.get("curriculum")
    }
    teacher_persona = compose_prompt(read_file("prompts/persona_teacher.md"), teacher_persona_params)
    teacher = Agent("assistant", teacher_persona)
    teacher.set_system_message(teacher_persona)

    student_persona = compose_prompt(read_file(load_prompt_path(State.get("persona"))), None)
    student = Agent("user", student_persona)
    student.set_system_message(student_persona)
    st.write(f"학생 프롬프트 : {student_persona}")

    if st.button("Start"):
        former_message = ""
        for _ in range(10):
            former_message = teacher.inference(former_message)
            st.write(f"선생님 : {former_message}")
            st.write(" - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            former_message = student.inference(former_message)
            st.write(f"학생 : {former_message}")
            st.write(" - - - - - - - - - - - - - - - - - - - - - - - - - - -")