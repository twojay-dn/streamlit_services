import streamlit as st
from src.Controllers import BaseController, inference_generation_hints, inference_generation_questions
from src.Views.Components import BaseColumns
from src.Models.Wordspool import WordsPool

controller = BaseController

def generation_hint_and_question(target_word, target_word_category, verbose : bool = False):
	controller.set("target_word", target_word, overwrite=True)
	controller.set("target_word_category", target_word_category, overwrite=True)
	hints = inference_generation_hints(target_word, 10)
	questions = inference_generation_questions(target_word_category, 10)
	if verbose:
		st.write(f"정답 단어: {target_word}")
		st.write(f"정답 단어 카테고리: {target_word_category}")
		st.write(f"힌트: {hints}")
		st.write(f"질문: {questions}")
	return hints, questions

def can_we_start_quiz():
	controller = BaseController
	condition = controller.get("target_word", None) is not None and controller.get("hints", None) is not None and controller.get("questions", None) is not None
	return condition

answer_word_key = "answer"
answer_word_category_key = "answer_category"
hints_key = "hints"
questions_key = "questions"
try_count_key = "try_count"
llm_key = "llm"
memory_key = "memory"
limit_try_count = 10

def generation_column():
	def text_input():
		st.write("정답 단어를 입력하거나")
		input_word = st.text_input(label="정답 단어", key="hint_text_input")
		input_word_category = st.text_input(label="정답 단어 카테고리", key="hint_text_category_input")
  
		if st.button("생성", key="hint_generate"):
			if input_word and input_word_category:
				controller.set(answer_word_key, input_word, overwrite=True)
				controller.set(answer_word_category_key, input_word_category, overwrite=True)
				hints, questions = generation_hint_and_question(input_word, input_word_category)
				controller.set(hints_key, hints, overwrite=True)
				controller.set(questions_key, questions, overwrite=True)
			else:
				st.error("정답 단어와 정답 단어 카테고리를 입력해주세요")
	
		if st.button("초기화", key="hint_reset"):
			controller.set(hints_key, None, overwrite=True)
			controller.set(questions_key, None, overwrite=True)
			controller.set(try_count_key, 0, overwrite=True)
			controller.set(memory_key, None, overwrite=True)
			controller.set(llm_key, None, overwrite=True)

	def random_generate_input():
		st.write("단어풀에서 랜덤하게 고르세요")
		if st.button("랜덤 생성", key="hint_random_generate"):
			target_word, target_word_category = WordsPool.get_random_word()
			controller.set(answer_word_key, target_word, overwrite=True)
			controller.set(answer_word_category_key, target_word_category, overwrite=True)
			hints, questions = generation_hint_and_question(target_word, target_word_category)
			controller.set(hints_key, hints, overwrite=True)
			controller.set(questions_key, questions, overwrite=True)
  
	c = BaseColumns([
		text_input,
		random_generate_input,
	])
	c.render()
	on = st.toggle("정답 및 생성된 질문/답변 보기")
	st.divider()
	if on:
		if can_we_start_quiz() == False:
			st.write("아직 게임을 시작하지 않았습니다.")
		else:
			st.write(f"정답 단어: {controller.get(answer_word_key)}")
			st.write(f"정답 단어 카테고리: {controller.get(answer_word_category_key)}")
			st.write(controller.get(hints_key))
			st.write(controller.get(questions_key))


from src.Controllers.LLM import OpenAIController
from src.Controllers.ChatMemory import MemoryController

def display_memory_on_chat(memory):
	if memory is None:
		return
	for message in memory.get_memory():
		st.chat_message(message["role"]).write(message["content"])

def init_quiz():
  try_count = controller.get(try_count_key, 0)
  llm = OpenAIController(
    "gpt-3.5-turbo",
    sysprompt_key="system_Quiz_type_00"
  )
  memory = MemoryController()
  return memory, llm, try_count

def is_able_init_quiz():
  return controller.get(try_count_key, 0) is None

def check_generation():
	hints = controller.get(hints_key)
	questions = controller.get(questions_key)
	return hints is None and questions is None

def chat_column():
	height = 650
	history_container = st.container(height=round(height * 0.8))
	input_container = st.container(height=round(height * 0.2))
	if is_able_init_quiz():
		memory, llm, try_count = init_quiz()
		controller.set(try_count_key, try_count, overwrite=True)
		controller.set(memory_key, memory, overwrite=True)
		controller.set(llm_key, llm, overwrite=True)
	else:
		memory = controller.get(memory_key)
		llm = controller.get(llm_key)
		try_count = controller.get(try_count_key)

	st.write(f"시도 횟수: {try_count} / {limit_try_count}")
	with input_container:
			if check_generation():
				pass
			else:
				st.chat_input("질문을 입력하세요")
				if st.button("힌트", key="chat_hint"):
					question_hints = controller.get(questions_key)
					question_list = question_hints.get("questions")
					hint_button_click(memory, question_list)
				controller.set(try_count_key, try_count + 1, overwrite=True)
		
	with history_container:
		if check_generation():
			st.chat_message("assistant").write("정답 단어를 입력하거나 단어풀에서 랜덤하게 고르세요")
		else:
			display_memory_on_chat(memory)

import random

def hint_button_click(memory, question_list):
	if question_list is None:
		memory.add_message("assistant", "아직 시작하지 않았습니다")
		return
	else:
		query = random.choice(question_list)
		memory.add_message("user", query)