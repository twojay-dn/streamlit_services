import streamlit as st
from src.Controllers import BaseController, TempController, inference_generation_hints, inference_generation_questions
from src.Views.Components import BaseColumns, ChatBoxComponent
from src.Models.Wordspool import WordsPool
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController
from src.utils import get_random_text

def init(temporary_controller : TempController = None, need_base_controller : bool = False):
  c = temporary_controller
  if c is None:
    if need_base_controller:
      c = BaseController
    else:
      c = TempController()
      
  def text_input():
    st.write("정답 단어를 입력하거나")
    if target_word := st.text_input(label="정답 단어", key="hint_text_input"):
      c.set("target_word", target_word, overwrite=True)
    if target_word_category := st.text_input(label="정답 단어 카테고리", key="hint_text_category_input"):
      c.set("target_word_category", target_word_category, overwrite=True)

  def random_generate_input():
    st.write("단어풀에서 랜덤하게 고르세요")
    if st.button("랜덤 생성", key="hint_random_generate"):
      target_word = WordsPool.get_random_word()
      c.set("target_word", target_word[0], overwrite=True)
      c.set("target_word_category", target_word[1], overwrite=True)

  def generate_hint_and_question(verbose : bool = False) -> None:
    if c.get("target_word", None) is not None:
      c.set("hints", inference_generation_hints(c.get("target_word"), 10), overwrite=True)
      c.set("questions", inference_generation_questions(c.get("target_word"), 10), overwrite=True)
      if verbose:
        if c.get("target_word", None) is not None:
          st.write(f"정답 단어: {c.get('target_word')}")
        if c.get("hints", None) is not None:
          st.write(c.get("hints"))
        if c.get("questions", None) is not None:
          st.write(c.get("questions"))
              
  temps = BaseColumns([
    text_input,
    random_generate_input
  ])
  temps.render()
  st.divider()
  if c.get("target_word", None) is not None:
    generate_hint_and_question(verbose=True)

# TODO : 이 안에서 퀴즈 구성에 필요한 플로우 구성해서 진행할 것
def print_llm_state(self, prompt, memory):    
    return "hello override"

def chat_part():
    BaseController.set_state("memory", MemoryController())
    llm = OpenAIController("gpt-3.5-turbo")
    llm.overwrite_call_to_inference(print_llm_state)
    BaseController.set_state("llm", llm)
    chatbox = ChatBoxComponent(
        memory=BaseController.get_state("memory"),
        llm=BaseController.get_state("llm")
    )
    chatbox.render()