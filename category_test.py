import streamlit as st
from typing import List, Dict, Any
import csv, os, random, json
from openai import OpenAI
from collections import Counter
from static_messages import *

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_answer_check(user_input: str, target_word: str) -> Dict[str, Any]:
    prompt = read_file(f"{os.getcwd()}/resource/prompt/check_answer_in_query.md")
    temp_input_dict = {
        "role": "user",
        "content": f"<answer_word>{target_word}</answer_word>\n<user_input>{user_input}</user_input>"
    }
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            temp_input_dict
        ],
        temperature=0.05,
        max_tokens=1000,
    )
    content = response.choices[0].message.content
    if "```" in content:
        content = content.replace("```json", "").replace("```", "")
    formed = json.loads(content)
    return formed

def main():
    st.title("LLM 카테고리 테스트")

    st.text_input("단어", key="word", on_change=lambda: st.session_state.update({"word": st.session_state.word}))
    st.text_input("카테고리", key="category", on_change=lambda: st.session_state.update({"category": st.session_state.category}))
    st.text_input("사용자 입력", key="user_input", on_change=lambda: st.session_state.update({"user_input": st.session_state.user_input}))
    st.number_input("반복 횟수", min_value=1, max_value=100, value=1, step=1, key="repeat_count")

    if st.button("테스트 시작"):
        target_word = st.session_state.word
        target_category = st.session_state.category
        user_input = st.session_state.user_input
        repeat_count = st.session_state.repeat_count

        results = []
        for i in range(repeat_count):
            answer_check = generate_answer_check(user_input, target_word)
            if answer_check["result"]:
                results.append(f"시행 {i + 1}: 정답입니다!")
            else:
                results.append(f"시행 {i + 1}: 오답입니다!")

        for result in results:
            st.write(result)

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()