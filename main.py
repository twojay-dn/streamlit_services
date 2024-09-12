import streamlit as st
from typing import List, Dict, Any
import csv, os, random, json
from openai import OpenAI
from collections import Counter
from static_messages import *

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
model_name = "gpt-4o-mini"

def init():
  st.session_state.setdefault("word", "")
  st.session_state.setdefault("category", "")
  st.session_state.setdefault("target_word", "")
  st.session_state.setdefault("target_category", "")
  st.session_state.setdefault("answer_input", "")
  st.session_state.setdefault("chat_history", [])
  st.session_state.setdefault("generated_hint", [])
  st.session_state.setdefault("generated_code_level_hint", {})
  st.session_state.setdefault("words", read_csv(f"{os.getcwd()}/resource/words.csv"))
  st.session_state.setdefault("ai_hint_dict", {})

  
def read_file(file_path : str) -> str:
  with open(file_path, "r", encoding = "utf-8") as file:
    return file.read()
  
def read_csv(file_path : str) -> List[Dict[str, Any]]:
  with open(file_path, "r", encoding = "utf-8") as file:
    reader = csv.DictReader(file)
    next(reader)  # 첫 줄(헤더) 건너뛰기
    return list(reader)

def generate_hint(target_word : str, target_category : str, count : int = 11) -> List[str]:
  target_word = target_word.lower()
  target_category = target_category.lower()
  prompt = read_file(f"{os.getcwd()}/resource/prompt/gen_hint_list.md")
  prompt = prompt.replace("{target_word}", target_word)
  prompt = prompt.replace("{target_category}", target_category)
  prompt = prompt.replace("{count}", str(count))
  response = client.chat.completions.create(
    model = model_name,
    messages = [
      {"role": "system", "content": prompt},
    ],
    temperature =  0.56,
    max_tokens = 1200,
    top_p = 0.95
  )
  content = response.choices[0].message.content
  if "```" in content:
    content = content.replace("```json","").replace("```","")
  result_list = json.loads(content)["hints"]
  return result_list

character_frequency_hint_format = "{key}가 {value}개 있어."

def convert_Counter_dict_info_to_sentence(counter_dict : Dict[str, int]) -> str:
  result = []
  for key, value in counter_dict.items():
    result.append(character_frequency_hint_format.format(key = key, value = value))
  return result

def generate_code_level_hint(target_word : str, target_category : str) -> Dict[str, Any]:
  target_word = target_word.lower()
  target_category = target_category.lower()
  result = {
    "first_letter" : target_word[0],
    "last_letter" : target_word[-1],
    "length" : len(target_word),
    "character_count" : convert_Counter_dict_info_to_sentence(dict(Counter(target_word))),
  }
  return result

def make_chat_systemp_prompt(target_word : str, target_category : str, hint : str) -> str:
  prompt = read_file(f"{os.getcwd()}/resource/prompt/main_instruction.md")
  prompt = prompt.replace("{content}", target_word)
  return prompt

def generate_chat_response(chat_history : List[Dict[str, Any]], target_word : str, target_category : str, hint : str) -> str:
  if "prompt" not in st.session_state:
    prompt = make_chat_systemp_prompt(target_word, target_category, hint)
    st.session_state.update({"prompt": prompt})
  messages = [{"role": "system", "content": st.session_state.prompt}]
  messages.extend(chat_history)
  response = client.chat.completions.create(
    model = model_name,
    messages = messages,
    temperature = 0.45,
    max_tokens = 1500,
    top_p = 0.95
  )
  result = response.choices[0].message.content
  print(f"chat_response_draft : {result}")
  return result

def generate_answer_check(user_input : str, target_word : str) -> bool:
  prompt = read_file(f"{os.getcwd()}/resource/prompt/check_answer_prompt.md")
  temp_input_dict = {
    "role" : "user",
    "content" : f"<answer_word>{target_word}</answer_word>\n<user_input>{user_input}</user_input>"
  }
  
  response = client.chat.completions.create(
    model = model_name,
    messages = [ 
      {"role": "system", "content": prompt},
      temp_input_dict
    ],
    temperature = 0.05,
    max_tokens = 1000,
  )
  content = response.choices[0].message.content
  if "```" in content:
    content = content.replace("```json","").replace("```","")
  formed = json.loads(content)
  print(f"formed : {formed}")
  return formed

def add_message_to_chat_history(role : str, content : str):
  st.session_state.update({"chat_history": st.session_state.chat_history + [{"role": role, "content": content}]})

def validate_answer(answer : str, submitted : str) -> bool:
  return True if answer == submitted else False

from typing import Callable

def retrier(func : Callable, condition_callable : Callable = None, required_args : List[str] = [], max_retry : int = 5, *args, **kwargs):
  if condition_callable is None:
    condition_callable = lambda res : True
  while True:
    try:
      res = func(*args, **kwargs)
      if condition_callable(res):
        return res
      else:
        raise Exception("condition_callable is not satisfied")
    except Exception as e:
      print(e)
      if max_retry == 0:
        raise Exception("max retry count exceeded")
      max_retry -= 1

def main():
  hint_container = st.container(height = 200)
  
  with hint_container:
    col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
    with col1:
      st.text_input("단어", key = "word", on_change = lambda: st.session_state.update({"word": st.session_state.word}))
      st.text_input("카테고리", key = "category", on_change = lambda: st.session_state.update({"category": st.session_state.category}))
    with col2:
      empty_space = st.container(height = 30, border = False)
      randomgen_button = st.button("랜덤 생성", key = "randomgen_button")
      customgen_button = st.button("커스텀 생성", key = "customgen_button")
      if randomgen_button:
        picked = random.choice(st.session_state.words)
        picked_word = picked["word"]
        picked_category = picked["category"]
        st.session_state.update({"target_word": picked_word})
        st.session_state.update({"target_category": picked_category})
        generated_hint_callable = lambda : generate_hint(picked_word, picked_category)
        generated_code_level_hint_callable = lambda : generate_code_level_hint(picked_word, picked_category)
        generated_hint = retrier(generated_hint_callable)
        generated_code_level_hint = retrier(generated_code_level_hint_callable)
        st.session_state.update({"generated_hint": generated_hint})
        st.session_state.update({"generated_code_level_hint": generated_code_level_hint})
      if customgen_button:
        generated_hint_callable = lambda : generate_hint(st.session_state.word, st.session_state.category)
        generated_code_level_hint_callable = lambda : generate_code_level_hint(st.session_state.word, st.session_state.category)
        generated_hint = retrier(generated_hint_callable)
        generated_code_level_hint = retrier(generated_code_level_hint_callable)
        st.session_state.update({"target_word": st.session_state.word})
        st.session_state.update({"target_category": st.session_state.category})
        st.session_state.update({"generated_hint": generated_hint})
        st.session_state.update({"generated_code_level_hint": generated_code_level_hint})
    with col3:
      regame_button = st.button("재시작", key = "regame_button")
      if regame_button:
        st.session_state.update({"chat_history": []})
        st.session_state.update({"generated_hint": []})
        st.session_state.update({"generated_code_level_hint": {}})
        st.session_state.update({"ai_hint_dict": {}})
        st.session_state.update({"prompt": None})
        st.rerun()

  col_chat, col_display_hint = st.columns([0.7, 0.3]) 
  user_turn_count = sum(1 for chat in st.session_state.chat_history if chat['role'] == 'user')
  turn_limit = 10
  if (randomgen_button or customgen_button) and len(st.session_state.chat_history) == 0:
    picked_hint = st.session_state.generated_hint.pop(len(st.session_state.generated_hint) - 1)
    add_message_to_chat_history("assistant", random.choice(start_messages) + "\n" + f"the hint is ... {picked_hint}")
  with col_chat:
    chat_history_container = st.container(height = 500)
    chat_container = st.container(height = 130)
    ai_hint_container = st.container(height = 200)
    with chat_history_container:
      for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
          st.write(chat["content"])
    with chat_container:
      if user_turn_count < turn_limit:
        chat_input = st.chat_input("채팅 입력")
        if chat_input:
          add_message_to_chat_history("user", chat_input)
          condition = lambda res : "result" in res
          answer_check_callable = lambda : generate_answer_check(st.session_state.word, chat_input)
          print(chat_input)
          answer_check = retrier(answer_check_callable, condition_callable=condition)
          if answer_check["result"]:
            add_message_to_chat_history("assistant", random.choice(correct_answer_messages) + "\n" + "Let's submit the answer in the input box.")
          else:
            picked_hint = st.session_state.generated_hint.pop(len(st.session_state.generated_hint) - 1)
            response_callable = lambda : generate_chat_response(st.session_state.chat_history, st.session_state.word, st.session_state.category, picked_hint)
            response = retrier(response_callable)
            response = f"{response}. {picked_hint}"
            add_message_to_chat_history("assistant", response)
          st.rerun()

        col_answer_input, col_submit_button, col_turn = st.columns([0.82, 0.1, 0.08])
        with col_answer_input:
          text_input = st.text_input(label="정답 입력", key="answer_input", label_visibility="collapsed")
        with col_submit_button:
          submit_button = st.button("제출", key = "submit_button")
          if text_input and submit_button:
            add_message_to_chat_history("user", text_input)
            result_validation_answer = validate_answer(text_input, st.session_state.target_word)
            if result_validation_answer:
              add_message_to_chat_history("assistant", random.choice(correct_answer_messages))
            else:
              add_message_to_chat_history("assistant", random.choice(wrong_answer_messages))
            st.rerun()
        with col_turn:
          st.write(f"{user_turn_count} / {turn_limit}")
      else:
        add_message_to_chat_history("assistant", f"{turn_limit}턴 초과")

    with ai_hint_container:
      col_hint_display, col_hint_button = st.columns([0.8, 0.2])
      with col_hint_display:
        if st.session_state.ai_hint_dict:
          st.write(st.session_state.ai_hint_dict)
        else:
          selected_hints_from_code_level_hint = []
          selected_hints_from_generated_hint = ""
          generated = st.session_state.randomgen_button or st.session_state.customgen_button
          if generated:
            if len(st.session_state.generated_code_level_hint) >= 2:
              reformed = list(st.session_state.generated_code_level_hint.items())
              selected_hints_from_code_level_hint = random.sample(reformed, 2)
            if len(st.session_state.generated_hint) >= 1:
              selected_hints_from_generated_hint = st.session_state.generated_hint.pop(0)
            ai_hint_dict = [
              selected_hints_from_code_level_hint[0],
              selected_hints_from_code_level_hint[1],
              selected_hints_from_generated_hint
            ]
            st.session_state.update({"ai_hint_dict": ai_hint_dict})
            st.rerun()
  with col_display_hint:
    hint_container = st.container(height = 930)
    with hint_container:
      st.write("힌트 표시창")
      st.write(f"정답 : {st.session_state.target_word}")
      st.write(f"카테고리 : {st.session_state.target_category}")
      st.write(st.session_state.generated_hint)
      st.write(st.session_state.generated_code_level_hint)
      
if __name__ == "__main__":
  st.set_page_config(layout="wide")
  init()
  main()