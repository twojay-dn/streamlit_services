import streamlit as st
from src.Controllers import BaseController, inference_generation_as_list
from src.Views.Components import BaseColumns
from src.Models.Wordspool import WordsPool
from src.Models.pydantic_models import QuestionList
import random

controller = BaseController
answer_word_key = "answer"
answer_word_category_key = "answer_category"
hints_key = "hints"
questions_key = "questions"
try_count_key = "try_count"
llm_key = "llm"
memory_key = "memory"
is_end_key = "is_end"
limit_try_count = 10

def generation_question_by_target_word(target_word, target_word_category):
	answer_questions = inference_generation_as_list(
		prompt_key="questions_generation_prompt_v3",
		target_list_class=QuestionList,
		model_name="gpt-3.5-turbo",
		params={"quiz_category": target_word, "count": 10}
	)
	category_questions = inference_generation_as_list(
		prompt_key="questions_generation_prompt_v3",
		target_list_class=QuestionList,
		model_name="gpt-3.5-turbo",
		params={"quiz_category": target_word_category, "count": 10}
	)
	# # 각 리스트에서 짝수 인덱스 항목만 선택
	answer_questions = answer_questions.get("questions")[::2]
	category_questions = category_questions.get("questions")[::2]
	# 두 리스트 합치기
	combined_questions = {
		"questions": answer_questions + category_questions
	}
	if combined_questions.get("questions") is None or len(combined_questions.get("questions")) != 10:
		st.error("생성 도중에 에러가 발생했습니다. 다시 시도해주세요")
	return combined_questions

def safe_run_quiz():
	questions = controller.get(questions_key)
	llm = controller.get(llm_key)
	memory = controller.get(memory_key)
	answer_word = controller.get(answer_word_key)
	answer_word_category = controller.get(answer_word_category_key)
	result = all([questions, llm, memory, answer_word, answer_word_category])
	if result is True and llm and "{quiz_answer}" in llm.system_prompt:
		llm.system_prompt = llm.system_prompt.replace("{quiz_answer}", answer_word)
	return result

def safe_display_quiz():
	questions = controller.get(questions_key)
	answer_word = controller.get(answer_word_key)
	answer_word_category = controller.get(answer_word_category_key)
	return all([questions, answer_word, answer_word_category])

def generation_button_callback(input_word, input_word_category):
	if input_word and input_word_category:
		controller.set(answer_word_key, input_word, overwrite=True)
		controller.set(answer_word_category_key, input_word_category, overwrite=True)
		questions = generation_question_by_target_word(input_word, input_word_category)
		controller.set(questions_key, questions, overwrite=True)
	else:
		st.error("정답 단어와 정답 단어 카테고리를 입력해주세요")	

def reset_button_callback():
	controller.set(answer_word_key, None, overwrite=True)
	controller.set(answer_word_category_key, None, overwrite=True)
	controller.set(questions_key, None, overwrite=True)
	controller.set(try_count_key, 0, overwrite=True)
	controller.set(memory_key, None, overwrite=True)
	controller.set(llm_key, None, overwrite=True)

def random_generation_callback():
	target_word, target_word_category = WordsPool.get_random_word()
	controller.set(answer_word_key, target_word, overwrite=True)
	controller.set(answer_word_category_key, target_word_category, overwrite=True)
	questions = generation_question_by_target_word(target_word, target_word_category)
	controller.set(questions_key, questions, overwrite=True)

def display_hint_and_question():
	st.write(f"정답 단어: {controller.get(answer_word_key)}")
	st.write(f"정답 단어 카테고리: {controller.get(answer_word_category_key)}")
	questions = controller.get(questions_key)
	controller.set("display_questions", questions.copy(), overwrite=True)
	st.write(controller.get('display_questions'))

def generation_column():
	def text_input():
		st.write("정답 단어를 입력하거나")
		input_word = st.text_input(label="정답 단어", key="hint_text_input")
		input_word_category = st.text_input(label="정답 단어 카테고리", key="hint_text_category_input")
		if st.button("생성", key="hint_generate"):
			generation_button_callback(input_word, input_word_category)
		if st.button("초기화", key="hint_reset"):
			reset_button_callback()

	def random_generate_input():
		st.write("단어풀에서 랜덤하게 고르세요")
		if st.button("랜덤 생성", key="hint_random_generate"):
			random_generation_callback()

	c = BaseColumns([
		text_input,
		random_generate_input,
	])
	c.render()
	on = st.toggle("정답 및 생성된 질문/답변 보기")
	st.divider()
	if on:
		if safe_display_quiz() == False:
			st.write("아직 게임을 시작하지 않았습니다.")
		else:
			display_hint_and_question()

from src.Controllers.LLM import OpenAIController
from src.Controllers.ChatMemory import MemoryController

def display_memory_on_chat():
	memory = controller.get(memory_key)
	if memory:
		for message in memory.get_memory():
			st.chat_message(message["role"]).write(message["content"])

def init_quiz():
	if is_need_init_quiz() is False:
		try_count = controller.get(try_count_key, 0)
		llm = OpenAIController(
			"gpt-3.5-turbo",
			sysprompt_key="system_Quiz_type_00"
		)
		memory = MemoryController()
		controller.set(try_count_key, try_count, overwrite=True)
		controller.set(memory_key, memory, overwrite=True)
		controller.set(llm_key, llm, overwrite=True)
		controller.set(is_end_key, False, overwrite=True)

def is_need_init_quiz():
	try_count = controller.get(try_count_key, 0)
	llm = controller.get(llm_key, None)
	memory = controller.get(memory_key, None)
	return all([try_count, llm, memory])

def get_random_welcome_message():
	welcome_messages = controller.get("welcome_messages")
	return random.choice(welcome_messages)

import re

def is_right_answer(
  prompt : str, 
  answer_word : str
) -> bool:
	if prompt is None or answer_word is None:
		return False
	prompt = prompt.lower()
	answer_word = answer_word.lower()
	text = re.sub(r'[^a-zA-Z0-9\s]', ' ', prompt)
	text = re.sub(r'\s+', ' ', text).strip()
	word_list = text.split()
	return answer_word in word_list



def response_right_word():
	import time
	time.sleep(1)
	pickup_correct = random.choice(controller.get("correct_messages"))
	return f"{pickup_correct} -  the answer is {controller.get(answer_word_key)}."

def quiz_logic():
	memory = controller.get(memory_key)
	llm : OpenAIController = controller.get(llm_key)
	try_count = controller.get(try_count_key)
	if try_count == 0:
		memory.add_message("assistant", get_random_welcome_message())
	if prompt := st.chat_input("질문을 입력하세요"):
		memory.add_message("user", prompt)
	if st.button("힌트", key="chat_hint"):
		prompt = hint_button_callback()
		memory.add_message("user", prompt)
	if prompt:
		if is_right_answer(prompt, controller.get(answer_word_key)):
			memory.add_message("assistant", response_right_word())
			controller.set(is_end_key, True, overwrite=True)
		else:
			response = llm.inference(prompt, memory)
			memory.add_message("assistant", response)
			controller.set(try_count_key, try_count + 1, overwrite=True)

def chat_column():
	height = 650
	history_container = st.container(height=round(height * 0.8))
	input_container = st.container(height=round(height * 0.2))
	init_quiz()
	try_count = controller.get(try_count_key)

	st.write(f"시도 횟수: {try_count} / {limit_try_count}")
	with input_container:
		if controller.get(is_end_key) is False:
			if safe_run_quiz() is False:
				st.chat_message("assistant").write("정답 단어를 입력하거나 단어풀에서 랜덤하게 고르세요")
			else:
				if try_count > limit_try_count:
					st.chat_message("assistant").write(f"시도 횟수가 모두 소진되었습니다. 정답은 다음과 같습니다: {controller.get(answer_word_key)}")
					controller.set(is_end_key, True, overwrite=True)
				else:
					quiz_logic()

	with history_container:
		display_memory_on_chat()

def hint_button_callback():
	question_list = controller.get(questions_key).get("questions")
	# 마지막 원소를 리스트에서 제거하고 반환
	prompt = question_list.pop() if question_list else None
	return prompt

# 작업 주안점
# 1. 힌트 제공기능 삭제 - v
# 2. 질문에서 더 쉬운 단어 활용 - v
# 3. 제시단어가 정답단어에 포함시, 정답 미인정으로 변경 - v
# 6. AI 찬스 시에 질문이 매력도 기준 오름차순으로 나오도록 수정 - v
# 5. 단어 오탐지, 단어 오발화 -v
# 4. 봇에서 외부 매개변수로 정답여부 프롬프트에 주입 -> 발화

