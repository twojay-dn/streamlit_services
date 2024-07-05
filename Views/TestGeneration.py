import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from States import State
from functools import wraps
from typing import Callable
from utils import read_file
import os

def render():
    tab1, tab2 = st.tabs(["커리큘럼 생성", "커리큘럼 체크"])
    with tab1:
        generation_tap()
    with tab2:
        check_tap()

def check_tap():
    st.write("아래와 같은 수업과정으로 동작할 수 있습니다.")
    st.write("---")  # 구분선 추가    
    st.write(State.get("curriculum") if State.get("curriculum") != "" else "생성된 커리큘럼이 없습니다.")

def generation_tap():
    col1, col2 = st.columns(2)
    State.set("curriculum", "")
      
    with col1:
        grade = st.selectbox("학년을 선택해주세요.", ["3학년", "4학년", "5학년", "6학년"])
        subject = st.selectbox("과목을 선택해주세요.", ["국어", "영어", "과학", "사회", "도덕"])
        unit = st.text_input("단원을 입력해주세요.")
        title = st.text_input("수업 주제를 입력해주세요.")
        State.set("grade", grade)
        State.set("subject", subject)
        State.set("title", title)
        State.set("unit", unit)
        
    with col2:
        inp = st.text_area("수업 내용을 입력해주세요.", height=200)
        State.set("content", inp)
        if st.button("생성 버튼"):
            button_callback(inp)

def validate_curriculum_generation(func : Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not State.get("grade") or \
            not State.get("subject") or \
            not State.get("title") or \
            not State.get("unit"):
            st.error("필요한 정보 중 하나가 비어있습니다.\n : 학년, 과목, 주제, 단원")
        else:
            func(*args, **kwargs)
    return wrapper

@validate_curriculum_generation
def button_callback(inp : str) -> None:
    gen_curriculum = call_to_generation_curriculum(inp)
    State.set("curriculum", gen_curriculum)
    st.write("커리큘럼이 생성되었습니다.")
    
def call_to_generation_curriculum(inp : str) -> str:
    prompt_params = {
        "grade" : State.get("grade"),
        "subject" : State.get("subject"),
        "title" : State.get("title"),
        "unit" : State.get("unit"),
        "content" : inp
    }
    hyperparameters = {
        "temperature" : 0.35,
        "api_key" : os.getenv("OPENAI_API_KEY")
    }
    caller = ChatOpenAI(**hyperparameters)
    prompt = PromptTemplate.from_template(read_file(f"{os.getcwd()}/prompts/gen_curriculum.md"))
    chain = prompt | caller
    return chain.invoke(input=prompt_params).content

