from typing import Any, Dict

class Data:
  def __init__(self, d : Dict[str, Any] = None):
    self.data = d

  def get(self, key : str):
    return self.data[key]
  
  def set(self, key : str, value : Any, is_override : bool = False):
    if key in self.data and not is_override:
      raise ValueError(f"Key {key} already exists")
    self.data[key] = value

  def turnoff_all_boolean(self):
    for i in self.data:
      if isinstance(self.data[i], bool):
        self.data[i] = False

  def turnon_all_boolean(self):
    for i in self.data:
      if isinstance(self.data[i], bool):
        self.data[i] = True
  
  def is_contain(self, key : str):
    return key in self.data.keys()

  def __str__(self):
    return str(self.data)

  def __repr__(self):
    return str(self.data)

  def __getitem__(self, key):
    return self.data[key]
  
class Retrier:
  @staticmethod
  def retry(func, max_try = 3, *args, **kwargs):
    for i in range(max_try):
      try:
        return func(*args, **kwargs)
      except Exception as e:
        print(f"Error: {e}")
        

from typing import List
from openai import OpenAI
import os
import streamlit as st
from utils import load_prompt


def inference(messages : List[Dict[str, str]], model_id : str, temperature : float, max_tokens : int, top_p : float, frequency_penalty : float, presence_penalty : float):
  client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
  res = client.chat.completions.create(
    model=model_id,
    messages=messages,
    temperature=temperature,
    max_tokens=max_tokens,
    top_p=top_p,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty
  )
  return res.choices[0].message.content
class AI_TUTOR:
  @staticmethod
  def pipeline(
    messages : List[Dict[str, str]],
    model_id : str,
    temperature : float,
    max_tokens : int,
    top_p : float,
    frequency_penalty : float,
    presence_penalty : float
  ):
    checker_prompt = load_prompt("check_answer_in_query")
    response_prompt = load_prompt("main_instruction")
    temp = [
      {"role": "system", "content": checker_prompt},
      *messages
    ]
    
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    res = client.chat.completions.create(
      model=model_id,
      messages=messages,
      temperature=temperature,
      max_tokens=max_tokens,
      top_p=top_p,
      frequency_penalty=frequency_penalty,
      presence_penalty=presence_penalty
    )
    return res.choices[0].message.content