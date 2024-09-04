from interface import Interface
from refresher import Refresher
import streamlit as st
from utils import load_wordpool, load_prompt
from openai import OpenAI
import random
from classes import Data, Retrier
import json

client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

def generate_syno_anto(data, target_word):
  prompt : str = load_prompt("gen_syno_anto")
  prompt = prompt.replace("{target_word}", target_word)
  res = client.chat.completions.create(
    model=data.get("model_id"),
    messages=[
      {"role": "system", "content": prompt},
    ],
    temperature=data.get("temperature"),
    max_tokens=1200,
    top_p=data.get("top_p"),
    frequency_penalty=data.get("frequency_penalty"),
    presence_penalty=data.get("presence_penalty")
  )
  return res.choices[0].message.content

def generate_hints(data, target_word, target_word_category, count : int = 11) -> str:
  prompt : str = load_prompt("gen_hint_list")
  prompt = prompt.replace("{target_word}", target_word)
  prompt = prompt.replace("{target_word_category}", target_word_category)
  prompt = prompt.replace("{count}", str(count))
  res = client.chat.completions.create(
    model=data.get("model_id"),
    messages=[
      {"role": "system", "content": prompt},
    ],
    temperature=data.get("temperature"),
    max_tokens=1200,
    top_p=data.get("top_p"),
    frequency_penalty=data.get("frequency_penalty"),
    presence_penalty=data.get("presence_penalty")
  )
  return res.choices[0].message.content

from collections import Counter

def create_calculated_hints(data, target_word, target_word_category):
  return {
    "target_word" : target_word,
    "target_word_category" : target_word_category,
    "words_count" : len(target_word),
    "start_char" : target_word[0],
    "end_char" : target_word[-1],
    "char_counter" : dict(Counter(target_word.lower())),
    "most_clear_hint" : data.get("hints").get("hints")[0]
  }

def gen_hint_list(data, target_word, target_word_category):
    hint_list : str = generate_hints(data, target_word, target_word_category)
    data.set("hints", json.loads(hint_list))

def check_user_input(data, input_text):
  if data.get("submit_button"):
    # TODO 정답체크 로직
    print(f"input_text: {input_text} | 정답체크로직")
    pass
  else:
    # 발화 처리 로직
    print(f"input_text: {input_text} | 발화처리로직")
    st.session_state.chat_history.append({"role": "user", "content": input_text})
    
    pass

def control_impl(data):
  if data.get("custom_hint_creation_button"):
    if data.get("target_word") and data.get("target_word_category"):
      Retrier.retry(gen_hint_list, data=data, target_word=data.get("target_word"), target_word_category=data.get("target_word_category"))
      Retrier.retry(gen_syno_anto, data=data, target_word=data.get("target_word"))
      result = create_calculated_hints(data, data.get("target_word"), data.get("target_word_category"), data.get("syno_anto"))
      data.set("calculated_hint_dict", result)
  if data.get("random_hint_creation_button"):
    target_word, target_word_category = random.choice(st.session_state.get("wordpool"))
    Retrier.retry(gen_hint_list, data=data, target_word=target_word, target_word_category=target_word_category)
    result = create_calculated_hints(data, target_word, target_word_category)
    data.set("calculated_hint_dict", result)
  if data.get("submit_text"):
    check_user_input(data, data.get("submit_text"))
  return data

def default_init_instruction():
  st.set_page_config(layout="wide")
  st.session_state.setdefault("chat_history", [])
  st.session_state.setdefault("wordpool", load_wordpool())
  if "submit_text" not in st.session_state:
    st.session_state["submit_text"] = ""
    
class Controller:
  @classmethod
  def run(cls, interface: Interface, refresher: Refresher):
    default_init_instruction()
    data : Data = interface.run()
    postprocessed_data = cls.controll(data)
    refresher.run(postprocessed_data)
    
  @classmethod
  def controll(cls, data):
    return control_impl(data)