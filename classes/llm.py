from typing import List, Dict, Any
import streamlit as st

class Memory:
  def __init__(self):
    self.memory : List[Dict[str, str]] = []

  def _add(self, role : str, content : str) -> None:
    self.memory.append({"role": role, "content": content})

  def add_user_message(self, content : str) -> None:
    self._add("user", content)

  def add_assistant_message(self, content : str) -> None:
    self._add("assistant", content)

  def get(self) -> List[Dict[str, str]]:
    return self.memory

  def clean(self) -> None:
    self.memory = []
    
  def __str__(self) -> str:
    return "\n".join([f"{message['role']}: {message['content']}" for message in self.memory])

from openai import OpenAI

class Openai_LLM_Client:
  def __init__(self, *, params : Dict[str, str] = {}, system_prompt : str = None):
    self.client = OpenAI(api_key=get_api_key())
    self.model_name = params["model_name"]
    self.model_params = {k: v for k, v in params.items() if k != "model_name"}
    self.system_prompt = system_prompt
    if system_prompt is None or len(system_prompt) == 0:
      raise ValueError("System prompt is empty")

  def inference(self, prompt : str, memory : Memory) -> str:
    temp_prompt = self.system_prompt.replace("{conversation}", str(memory))
    print(temp_prompt)
    response = self.client.chat.completions.create(
      model=self.model_name,
      messages=[{"role": "user", "content": temp_prompt}],
      **self.model_params
    )
    return response.choices[0].message.content

def get_api_key() -> str:
  return st.secrets.OPENAI_API_KEY