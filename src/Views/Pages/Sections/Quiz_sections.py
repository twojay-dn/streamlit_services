import streamlit as st
from src.Controllers import BaseController, TempController, inference_generation_hints, inference_generation_questions
from src.Views.Components import BaseColumns, ChatBoxComponent
from src.Models.Wordspool import WordsPool
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController
import random















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
	if can_we_start_quiz() is False:
		generate_hint_and_question(verbose=True)

def quiz_flow(self, prompt, memory ):
	answer = BaseController.get("target_word")
	hints = BaseController.get("hints")
	questions = BaseController.get("questions")
	if hints is None or questions is None:
		return "hints or questions is None, return 'Init' page......"
	else:
		hints = hints.get("hints")
		questions = questions.get("questions")
	if BaseController.get("try_count") > 10:
		return f"Your try count is over 10, return 'Init' page....."
	if is_contains_answer(prompt, answer):
		import time
		time.sleep(1)
		pickup_correct = random.choice(BaseController.get("correct_messages"))
		return f"{pickup_correct} - the answer is {answer}."
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
		pickup_hint = random.choice(hints)
		BaseController.set("try_count", BaseController.get("try_count") + 1)
		return f"{response} - {pickup_hint}"

from re import sub
def is_contains_answer(text : str, answer : str) -> bool:
	if text is None or answer is None:
		return False
	text = sub(r'[^\w\s]', ' ', text)
	return answer in text

from src.Views.Components import BaseButton

def use_question_hint():
	questions = BaseController.get("questions").get("questions")
	assert isinstance(questions, list), "questions must be a list"
	pickup_question = random.choice(questions)
	BaseController.set("used_question_hint", pickup_question, overwrite=True)
	print(pickup_question)

def clear_quiz(chatbox, delete_quiz : bool = True):
	if delete_quiz:
		BaseController.delete("target_word")
		BaseController.delete("hints")
		BaseController.delete("questions")
	BaseController.delete("memory")
	BaseController.delete("llm")
	chatbox.clear_history()

def can_we_start_quiz():
	controller = BaseController
	condition = controller.get("target_word", None) is not None and controller.get("hints", None) is not None and controller.get("questions", None) is not None
	return condition

def chat_part():
	BaseController.set("try_count", 0)
	if BaseController.get("memory", None) is None:
		BaseController.set("memory", MemoryController())
	if BaseController.get("llm", None) is None:
		llm = OpenAIController("gpt-3.5-turbo", sysprompt_key="system_Quiz_type_00")
		llm.overwrite_call_to_inference(quiz_flow)
		BaseController.set("llm", llm)
	BaseButton("힌트", use_question_hint).render()
	chatbox = ChatBoxComponent(
		memory=BaseController.get("memory"),
		llm=BaseController.get("llm"),
		first_assistant_start=True
	)
	BaseButton("초기화", lambda : clear_quiz(chatbox, delete_quiz=False)).render()
	if can_we_start_quiz():
		chatbox.set_assistant_start_message(random.choice(BaseController.get("welcome_messages")))
		if BaseController.get("used_question_hint", None) is not None:
			chatbox.set_static_response(BaseController.get("used_question_hint"))
			BaseController.delete("used_question_hint")
		chatbox.render()
	else:
		chatbox.set_assistant_start_message("정답 단어를 입력하거나 단어풀에서 랜덤하게 고르세요")
		chatbox.render()