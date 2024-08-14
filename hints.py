import streamlit as st
import os
from typing import Dict, Any
from utils import read_file
from classes import Data
from messages import get_random_answer_word

def interface(component = st, state_manager = st.session_state) -> Dict[str, Any]:
    # 질문 힌트 생성
    component.write("질문 힌트 생성")
    custom_answer_word = component.text_input("유저 입력 정답 단어", value="")
    custom_answer_category = component.text_input("유저 입력 정답 카테고리", value="")
    col1, col2, col3 = component.columns([0.05, 0.15, 0.8])
    with col1:
        clicked_generation_button = component.button("생성")
    with col2:
        clicked_random_selection_and_generation_button = component.button("랜덤 선택 및 생성")
    with col3:
        pass
    return Data({
        "custom_answer_word": custom_answer_word,
        "custom_answer_category": custom_answer_category,
        "clicked_generation_button": clicked_generation_button,
        "clicked_random_selection_and_generation_button": clicked_random_selection_and_generation_button
    })

from openai import OpenAI
import json

def question_generation(target_word, target_category, count : int = 10, state_manager = st.session_state):
    prompt = read_file(f"{os.getcwd()}/resource/prompts/gen_question_list.md")
    prompt = prompt.replace("[count]", str(count))
    prompt = prompt.replace("[target_category]", target_category)
    prompt = prompt.replace("[target_word]", target_word)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=state_manager.get("model"),
        messages=[{"role": "user", "content": prompt}],
        temperature=state_manager.get("temperature"),
        max_tokens=500,
        top_p=state_manager.get("top_p"),
        frequency_penalty=state_manager.get("frequency_penalty"),
        presence_penalty=state_manager.get("presence_penalty")
    )
    created_json = response.choices[0].message.content
    created = json.loads(created_json)
    return created["questions"]

from typing import Callable

def trier(func, max_tries : int = 3, condition : Callable = lambda x: x is not None, verbose : bool = True):
    for i in range(max_tries):
        try:
            result = func()
            if condition(result):
                return result
            else:
                raise Exception("조건 불만족")
        except Exception as e:
            if verbose:
                print(f"{i}번째 시도 실패: {e}")
    return None

def hints(component = st, state_manager = st.session_state):
    inputed_by_interface = interface(component, state_manager)

    if inputed_by_interface.get("clicked_random_selection_and_generation_button"):
        word, category = get_random_answer_word()
        count = 10
        generated = trier(
            func=lambda: question_generation(
                word, 
                category,
                count,
            ),
            condition=lambda x: type(x) == list and len(x) == count,
            verbose=True
        )
        state_manager["generated_questions"] = generated
        state_manager["target_word"] = word
        state_manager["target_category"] = category
    elif inputed_by_interface.get("clicked_generation_button"):
        count = 10
        generated = trier(
            func=lambda: question_generation(
                inputed_by_interface.get("custom_answer_word"), 
                inputed_by_interface.get("custom_answer_category"),
                count,
            ),
            condition=lambda x: type(x) == list and len(x) == count,
            verbose=True
        )
        print(generated)
        state_manager["generated_questions"] = generated
        state_manager["target_word"] = inputed_by_interface.get("custom_answer_word")
        state_manager["target_category"] = inputed_by_interface.get("custom_answer_category")
    if "generated_questions" in state_manager:
        component.write(f"정답: {state_manager['target_word']}")
        component.write(f"카테고리: {state_manager['target_category']}")
        component.write("질문 리스트")
        if state_manager.get("generated_questions") is None:
            component.error("생성에 실패했습니다. 다시 시도해주세요.")
        else:
            component.write(state_manager['generated_questions'])

