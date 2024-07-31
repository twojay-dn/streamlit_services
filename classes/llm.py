from typing import List, Dict, Any
import streamlit as st
from openai import OpenAI
from abc import ABC, abstractmethod
import utils

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
  
  def __len__(self) -> int:
    return len(self.memory)


class Model_client(ABC):
  def __init__(self, *, params : Dict[str, str] = {}, system_prompt : str = None):
    self.model_name = params["model_name"]
    self.model_params = {k: v for k, v in params.items() if k != "model_name"}
    self.system_prompt = system_prompt
    if system_prompt is None or len(system_prompt) == 0:
      raise ValueError("System prompt is empty")

class Openai_LLM_Client(Model_client):
  def __init__(self, *, params : Dict[str, str] = {}, system_prompt : str = None):
    super().__init__(params=params, system_prompt=system_prompt)
    self.client = OpenAI(api_key=get_api_key())

  # prompt text 자체는 매개변수로 안받음.
  # prompt text를 Memory에 넣어주는 건 View (streamlit interface)의 권한으로 넘김
  def inference_with_memory(self, memory : Memory) -> str:
    temp_prompt = utils.insert_parameters(self.system_prompt, {"conversation" : str(memory)})
    response = self.client.chat.completions.create(
      model=self.model_name,
      messages=[{"role": "user", "content": temp_prompt}],
      **self.model_params
    )
    return response.choices[0].message.content

  def inference_with_prompt(self, prompt : str) -> str:
    response = self.client.chat.completions.create(
      model=self.model_name,
      messages=[{"role": "user", "content": prompt}],
      **self.model_params
    )
    return response.choices[0].message.content
  
  def generate_image(self, params : Dict[str, str]) -> str:
    if "model" not in params:
      params["model"] = self.model_name
    if "prompt" not in params:
      raise ValueError("Prompt is empty")
    response = self.client.images.generate(
      model=self.model_name,
      **params
    )
    return response.data[0].url

def get_api_key() -> str:
  return st.secrets.OPENAI_API_KEY

def chat_inference(model_client : Model_client, memory : Memory) -> str:
  return model_client.inference_with_memory(memory)

def single_inference(model_client : Model_client, prompt : str) -> str:
  return model_client.inference_with_prompt(prompt)

# JSON 파싱 이후 후처리 함수의 형식 지정
# 파싱되어서 json으로 변환한 뒤에 추가적인 작업을 하고자 할 때,
# JSON_Parse_PostProcessor을 준수하는 콜백함수를 JSON_Combiner.parse_according_JSON()에 전달해야 함
# 전반적으로 타이핑이 이후에도 자유로울 수 있도록 Protocol을 상속해서 PostProcessor를 정의하고
# 이후 요구되는 자료형에 맞춰 상속받아서 Callback의 형태를 정의하는 방식으로 진행함

from typing import Protocol
class PostProcessor(Protocol):
  def __call__(self, parsed : Any) -> Any:
    ...

class JSON_Parse_PostProcessor(PostProcessor):
  def __call__(self, parsed : Dict[str, Any]) -> Dict[str, Any]:
    ...

class JSON_Combiner:
  @staticmethod
  def validate(json_string : str) -> bool:
    try:
      parsed = JSON_Combiner.parse_JSON_to_dict(json_string)
      if parsed is None:
        return False
      return True
    except Exception as e:
      print(f"error : {e}")
      return False

  @staticmethod
  def parse_JSON_to_dict(response : str, post_processor : JSON_Parse_PostProcessor = None) -> Dict[str, Any]:
    if response is None:
      return None
    if "```" in response:
      response = response.replace("```json\n", "").replace("\n```", "")
    parsed = json.loads(response)
    if post_processor is not None:
      parsed = post_processor(parsed)
    return parsed

from enum import Enum, auto

class CONDITION_FORMAT(Enum):
  JSON = auto()
  DICT = auto()
  STRING = auto()

import json, functools
class Retrier:
  retry_error_message = "응답 생성에 실패했습니다. 다시 시도해 주세요."
  retry_count_parameter_error_message = "max_tries는 0보다 커야 합니다"
  
  @staticmethod
  def retry_on_invalid_response(
    max_tries=3,
    condition_format : CONDITION_FORMAT = None,
    post_processor : PostProcessor = None,
    need_to_raise_error : bool = True
  ):
    if max_tries <= 0:
      raise ValueError(Retrier.retry_count_parameter_error_message)
    def decorator(func):
      @functools.wraps(func)
      def wrapper(*args, **kwargs):
        tries = max_tries
        while tries >= 0:
          if tries == 0:
            if need_to_raise_error:
              raise RuntimeError(Retrier.retry_error_message)
            else:
              st.error(Retrier.retry_error_message)
              return None
          else:
            tries -= 1
          response = func(*args, **kwargs)
          if condition_format is not None:
            if condition_format == CONDITION_FORMAT.JSON:
              if JSON_Combiner.validate(response):
                parsed = JSON_Combiner.parse_JSON_to_dict(response, post_processor)
                return parsed
            elif condition_format == CONDITION_FORMAT.DICT:
              if isinstance(response, dict):
                return response
            elif condition_format == CONDITION_FORMAT.STRING:
              if isinstance(response, str):
                return response
      return wrapper
    return decorator
