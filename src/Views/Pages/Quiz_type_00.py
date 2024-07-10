import streamlit as st
from src.Controllers import BaseController, TempController, inference_generation_hints
from src.Views.Components import render_page, ChatBoxComponent, BaseTabs, BaseColumns
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController
from src.Models.Wordspool import WordsPool
from src.utils import get_random_text



def generate_hints():
    tc = TempController()
    
    def text_input():
        st.write("정답 단어를 입력하거나")
        if target_word := st.text_input(label="정답 단어"):
            tc.set("target_word", target_word)
            tc.set("hints", inference_generation_hints(tc.get("target_word"), 10))

    def random_generate():
        st.write("단어풀에서 랜덤하게 고르세요")
        if st.button("랜덤 생성"):
            target_word = WordsPool.get_random_word()
            tc.set("target_word", target_word)
            tc.set("hints", inference_generation_hints(tc.get("target_word"), 10))

    temps = BaseColumns([
        text_input,
        random_generate
    ])
    temps.render()
    if tc.get("hints", None) is not None:
        st.write(tc.get("hints"))

def chat_part():
    BaseController.set_state("memory", MemoryController())
    BaseController.set_state("llm", OpenAIController("gpt-3.5-turbo"))
    chatbox = ChatBoxComponent(
        memory=BaseController.get_state("memory"),
        llm=BaseController.get_state("llm")
    )
    chatbox.render()

@render_page(name="Quiz_type_00")
def page():
    tabs = BaseTabs([
        ("Generate Hints", generate_hints),
        ("Chat", chat_part)
    ])
    tabs.render()