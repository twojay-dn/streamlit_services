import streamlit as st
from src.Controllers import TempController, inference_generation_hints, inference_generation_questions
from src.Views.Components import BaseColumns
from src.Models.Wordspool import WordsPool


def generate_hints():
    tc = TempController()
    
    def text_input():
        st.write("정답 단어를 입력하거나")
        if target_word := st.text_input(label="정답 단어"):
            tc.set("target_word", target_word, overwrite=True)
            tc.set("hints", inference_generation_hints(tc.get("target_word"), 10), overwrite=True)

    def random_generate():
        st.write("단어풀에서 랜덤하게 고르세요")
        if st.button("랜덤 생성"):
            target_word = WordsPool.get_random_word()
            tc.set("target_word", target_word, overwrite=True)
            tc.set("hints", inference_generation_hints(tc.get("target_word"), 10), overwrite=True)

    temps = BaseColumns([
        text_input,
        random_generate
    ])
    temps.render()
    st.divider()
    if tc.get("target_word", None) is not None:
        st.write(f"정답 단어: {tc.get('target_word')}")
    st.divider()
    if tc.get("hints", None) is not None:
        st.write(tc.get("hints"))
        

def generate_questions():
    tc = TempController()
    
    def text_input():
        st.write("정답 단어를 입력하거나")
        if target_word := st.text_input(label="정답 단어"):
            tc.set("target_word", target_word, overwrite=True)
            tc.set("questions", inference_generation_questions(tc.get("target_word"), 10), overwrite=True)

    def random_generate():
        st.write("단어풀에서 랜덤하게 고르세요")
        if st.button("랜덤 생성"):
            target_word = WordsPool.get_random_word()
            tc.set("target_word", target_word, overwrite=True)
            tc.set("questions", inference_generation_questions(tc.get("target_word"), 10), overwrite=True)

    temps = BaseColumns([
        text_input,
        random_generate
    ])
    temps.render()
    st.divider()
    if tc.get("target_word", None) is not None:
        st.write(f"정답 단어: {tc.get('target_word')}")
    st.divider()
    if tc.get("questions", None) is not None:
        st.write(tc.get("questions"))
        

