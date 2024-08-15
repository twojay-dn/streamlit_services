import streamlit as st
from classes import Data, ChatMemory
from messages import get_random_welcome_message, get_random_correct_message

def data_init(state_manager : st.session_state = st.session_state):
	state_manager.setdefault("is_answer_mode", False)
	state_manager.setdefault("try_count", 0)
	state_manager.setdefault("try_count_limit", 10)
	state_manager.setdefault("answer_word", "")
	state_manager.setdefault("chat_memory", ChatMemory())
	state_manager.setdefault("is_end", False)
	state_manager.setdefault("question_hint_index", 0)

def data_reinit(state_manager : st.session_state = st.session_state):
    state_manager["try_count"] = 0
    state_manager["question_hint_index"] = 0
    state_manager["is_end"] = False
    state_manager["chat_memory"] = ChatMemory()
    state_manager["generated_questions"] = []
    state_manager["target_word"] = ""
    state_manager["target_category"] = ""
    state_manager["answer_word"] = ""

def display_history(component = st, state_manager : st.session_state = st.session_state):
    for message in state_manager.get("chat_memory").get_messages():
        with component.chat_message(message["role"]):
            component.markdown(message["content"])

def chat_interface(component = st, state_manager : st.session_state = st.session_state):
    col1, col2 = component.columns([0.5, 0.5])
    restart_button = component.button("다시 시작", key="restart_button")
    if restart_button:
        data_init(state_manager)
    with col2:
        if state_manager.get("generated_questions"):
            component.write("질문 힌트 리스트 :")
            component.write(state_manager.get("generated_questions"))
            component.write(f"정답 : {state_manager.get('target_word')}")
            component.write(f"정답 카테고리 : {state_manager.get('target_category')}")
        else:
            component.error("질문 힌트가 없습니다.")
    with col1:
        history_container = component.container(height=600)
        input_container = component.container(height=72)
        answer_container = component.container(height=72)
        with input_container:
            col1, col2 = component.columns([0.88, 0.12])
            with col1:
                input_text = component.chat_input("Input your text", key="input_text")
            with col2:
                question_hint_button = component.button("질문 힌트", key="question_hint_button")
        with answer_container:
            answer_input = component.chat_input("Input your answer", key="answer_input")
        return Data({
            "input_text" : input_text,
            "answer_input" : answer_input,
            "answer_input": answer_input or None,
            "history_container": history_container,
            "question_hint_button": question_hint_button,
            "restart_button": restart_button
        })

def quiz_controller(component = st, state_manager : st.session_state = st.session_state, input_data : Data = None):
    # 리스트 초기화
    if input_data.get("restart_button") == True:
        data_reinit(state_manager)
        return
    # 정답 맞추었을 시
    if state_manager.get("is_end") == True:
        component.success(f"이미 정답을 맞추었습니다. 정답은 {state_manager.get('target_word')}입니다.")
        return
    # 턴수 초과시
    if state_manager.get("try_count") > state_manager.get("try_count_limit"):
        component.error(f"턴 수 초과, 정답은 {state_manager.get('target_word')}입니다.")
        return
    # 질문 탭에서 정답 입력시
    if state_manager.get("generated_questions") is None:
        component.error("질문 힌트가 없습니다. 먼저, 정답 단어를 설정하고 질문 힌트를 생성해주세요.")
        return
    # 게임 처음 시작시
    if state_manager.get("try_count") == 0 and state_manager.get("chat_memory").get_messages() == []:
        state_manager.get("chat_memory").add_message(role="assistant", content=get_random_welcome_message())
        return
    # 질문 힌트 버튼 클릭시
    if input_data.get("question_hint_button"):
        state_manager.get("chat_memory").add_message(role="user", content=get_random_question_hint_message())
        res = react_user_input(state_manager.get("chat_memory"), state_manager)
        state_manager.get("chat_memory").add_message(role="assistant", content=res)
    # 정답모드 정답 입력시
    if input_data.get("answer_input"):
        input_data.set("answer_mode_button", False)
        # 정답일시
        if is_right_answer(input_data.get("answer_input"), state_manager.get("target_word")):
            state_manager.get("chat_memory").add_message(role="user", content=input_data.get("answer_input"))
            state_manager.get("chat_memory").add_message(role="assistant", content=f"{get_random_correct_message()}. the answer is {state_manager.get('target_word')}.")
            state_manager["is_end"] = True
        else:
            # 정답이 아닐시
            state_manager.get("chat_memory").add_message(role="user", content=input_data.get("answer_input"))
            res = react_user_input(state_manager.get("chat_memory"), state_manager)
            state_manager.get("chat_memory").add_message(role="assistant", content=res)
    # 유저 입력시
    if input_data.get("input_text"):
        user_input = input_data.get("input_text")
        state_manager.get("chat_memory").add_message(role="user", content=user_input)
        res = react_user_input(state_manager.get("chat_memory"), state_manager)
        state_manager.get("chat_memory").add_message(role="assistant", content=res)
    state_manager["try_count"] = state_manager.get("try_count") + 1

def get_random_question_hint_message(state_manager : st.session_state = st.session_state):
    hint_index = state_manager.get("question_hint_index")
    if hint_index >= len(state_manager.get("generated_questions")):
        st.error("사용할 수 있는 질문 힌트가 없습니다.")
        return
    question_hint = state_manager.get("generated_questions")[hint_index]
    state_manager["question_hint_index"] = hint_index + 1
    return question_hint

from openai import OpenAI
import os 

@st.cache_data
def get_system_prompt(path : str) -> str:
    with open(path, "r") as file:
        return file.read()

def react_user_input(memory: ChatMemory, state_manager : st.session_state = st.session_state):
    client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
    system_prompt = get_system_prompt(f"{os.getcwd()}/resource/prompts/quiz_agent_instructions.md")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_prompt}] + memory.get_messages(),
        temperature=state_manager.get("temperature"),
        max_tokens=state_manager.get("max_tokens"),
        top_p=state_manager.get("top_p"),
        frequency_penalty=state_manager.get("frequency_penalty"),
        presence_penalty=state_manager.get("presence_penalty"),
    )
    return response.choices[0].message.content

def is_right_answer(prompt : str, answer_word : str) -> bool:
    return prompt is not None and prompt.lower() == answer_word.lower()

def quiz(component = st, state_manager : st.session_state = st.session_state):
    data_init(state_manager)
    input_data = chat_interface(component, state_manager)
    quiz_controller(component, state_manager, input_data)
    with input_data.get("history_container"):
        display_history(component, state_manager)
    component.write(f"현재 턴 수 : {state_manager.get('try_count')} / {state_manager.get('try_count_limit')}")