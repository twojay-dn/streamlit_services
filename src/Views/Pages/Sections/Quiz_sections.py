import streamlit as st
from src.Controllers import BaseController, TempController, inference_generation_hints, inference_generation_questions
from src.Views.Components import BaseColumns, ChatBoxComponent
from src.Models.Wordspool import WordsPool
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController

def init(temporary_controller : TempController = None, need_base_controller : bool = False):
	controller = temporary_controller
	if controller is None:
		if need_base_controller:
			controller = BaseController
		else:
			controller = TempController()

	def text_input():
		st.write("정답 단어를 입력하거나")
		if target_word := st.text_input(label="정답 단어", key="hint_text_input"):
			controller.set("target_word", target_word, overwrite=True)
		if target_word_category := st.text_input(label="정답 단어 카테고리", key="hint_text_category_input"):
			controller.set("target_word_category", target_word_category, overwrite=True)

	def random_generate_input():
		st.write("단어풀에서 랜덤하게 고르세요")
		if st.button("랜덤 생성", key="hint_random_generate"):
			target_word = WordsPool.get_random_word()
			controller.set("target_word", target_word[0], overwrite=True)
			controller.set("target_word_category", target_word[1], overwrite=True)

	def generate_hint_and_question(verbose : bool = False) -> None:
		if controller.get("target_word", None) is not None:
			controller.set("hints", inference_generation_hints(controller.get("target_word"), 10), overwrite=True)
			controller.set("questions", inference_generation_questions(controller.get("target_word_category"), 10), overwrite=True)
			if verbose:
				if controller.get("target_word", None) is not None:
					st.write(f"정답 단어: {controller.get('target_word')}")
				if controller.get("target_word_category", None) is not None:
					st.write(f"정답 단어 카테고리: {controller.get('target_word_category')}")
				if controller.get("hints", None) is not None:
					st.write(controller.get("hints"))
				if controller.get("questions", None) is not None:
					st.write(controller.get("questions"))

	temps = BaseColumns([
		text_input,
		random_generate_input
	])
	temps.render()
	st.divider()
	if controller.get("target_word", None) is not None:
		generate_hint_and_question(verbose=True)

import random
def quiz_flow(self, prompt, memory):
  answer = BaseController.get("target_word")
  hints = BaseController.get("hints").get("hints")
  questions = BaseController.get("questions").get("questions")
  print(answer, hints, questions)
  filleter_none_list = list(filter(lambda v: v is None, [answer, hints, questions]))
  if len(filleter_none_list) != 0:
    raise ValueError(f"Please set the target word first. : {filleter_none_list}")
  if BaseController.get("try_count") > 10:
    return f"You wrong. Let's think carefully about this. - {pickup_hint}"
  pickup_hint = random.choice(hints)
  if is_contains_answer(prompt, answer):
    return f"You correct. the answer is {answer}."
  else:
    messages = memory.get_memory()
    self.insert_prompt_parameters({
			"quiz_answer" : answer
    })
    if self.system_prompt is not None:
      messages = [{"role": "system", "content": self.system_prompt}] + messages
    response = self.client.chat.completions.create(
			model=self.model,
			messages=messages
		)
    response = response.choices[0].message.content
    BaseController.set("try_count", BaseController.get("try_count") + 1)
    return f"{response} - {pickup_hint}"

from re import sub
def is_contains_answer(text : str, answer : str) -> bool:
	text = sub(r'[^\w\s]', ' ', text)
	return answer in text

def chat_part():
	BaseController.delete("memory")
	BaseController.delete("llm")
	BaseController.set("try_count", 0)
	BaseController.set("memory", MemoryController())
	llm = OpenAIController("gpt-3.5-turbo", sysprompt_key="system_Quiz_type_00")
	llm.overwrite_call_to_inference(quiz_flow)
	BaseController.set("llm", llm)
	chatbox = ChatBoxComponent(
		memory=BaseController.get("memory"),
		llm=BaseController.get("llm")
	)
	chatbox.render()