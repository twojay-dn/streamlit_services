from interface import Interface
from refresher import Refresher
import streamlit as st
from utils import load_wordpool, load_prompt
from openai import OpenAI
import random
from classes import Data
import json

client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

def generate_hints(data, target_word, target_word_category, count : int = 11):
  prompt = load_prompt("gen_hint_list")
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
  print(res.choices[0].message.content)
  return res.choices[0].message.content

def control_impl(data):
  if data.get("custom_hint_creation_button"):
    if data.get("target_word") and data.get("target_word_category"):
      hint_list = generate_hints(data, data.get("target_word"), data.get("target_word_category"))
      hint_list = json.loads(hint_list)
      data.set("hints", hint_list)
  if data.get("random_hint_creation_button"):
    target_word, target_word_category = random.choice(st.session_state.get("wordpool"))
    hint_list = generate_hints(data, target_word, target_word_category)
    hint_list = json.loads(hint_list)
    data.set("hints", hint_list)
  if data.is_contain("hints"):
    print(data.get("hints"))
    data.get("generated_hint_list_display_position").write(data.get("hints"))
  return data

def default_init_instruction():
  st.set_page_config(layout="wide")
  st.session_state.setdefault("chat_history", [])
  st.session_state.setdefault("wordpool", load_wordpool())

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