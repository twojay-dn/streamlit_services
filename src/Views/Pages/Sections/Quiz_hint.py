import streamlit as st
from src.Controllers import TempController, inference_generation_hints, inference_generation_questions
from src.Views.Components import BaseColumns
from src.Models.Wordspool import WordsPool
from src.utils import get_random_text


def generate_hints(temporary_controller : TempController = None):
	if tc := temporary_controller is None:
		tc = TempController()
	
	def text_input():
		st.write("정답 단어를 입력하거나")
		if target_word := st.text_input(label="정답 단어", key="hint_text_input"):
			tc.set("target_word", target_word, overwrite=True)
			tc.set("hints", inference_generation_hints(tc.get("target_word"), 10), overwrite=True)

	def random_generate():
		st.write("단어풀에서 랜덤하게 고르세요")
		if st.button("랜덤 생성", key="hint_random_generate"):
			target_word, target_word_category = WordsPool.get_random_word()
			tc.set("target_word", target_word, overwrite=True)
			tc.set("target_word_category", target_word_category, overwrite=True)
			tc.set("hints", inference_generation_hints(tc.get("target_word"), 10), overwrite=True)

	temps = BaseColumns([
		text_input,
		random_generate
	])
	temps.render()
	st.divider()
	if tc.get("target_word", None) is not None:
		st.write(f"정답 단어: {tc.get('target_word')}")
	if tc.get("target_word_category", None) is not None:
		st.write(f"정답 단어 카테고리: {tc.get('target_word_category')}")
	if tc.get("hints", None) is not None:
		st.write(tc.get("hints"))
		

def generate_questions(temporary_controller : TempController = None):
	if tc := temporary_controller is None:
		tc = TempController()
		
	def text_input():
		st.write("정답 단어를 입력하거나")
		if target_word := st.text_input(label="정답 단어", key="question_text_input"):
			tc.set("target_word", target_word, overwrite=True, )
			tc.set("questions", inference_generation_questions(tc.get("target_word"), 10), overwrite=True)

	def random_generate():
		st.write("단어풀에서 랜덤하게 고르세요")
		if st.button("랜덤 생성", key="question_random_generate"):
			target_word, target_word_category = WordsPool.get_random_word()
			tc.set("target_word", target_word, overwrite=True)
			tc.set("target_word_category", target_word_category, overwrite=True)
			tc.set("questions", inference_generation_questions(tc.get("target_word_category"), 10), overwrite=True)

	temps = BaseColumns([
		text_input,
		random_generate
	])
	temps.render()
	st.divider()
	if tc.get("target_word", None) is not None:
		st.write(f"정답 단어: {tc.get('target_word')}")
	if tc.get("target_word_category", None) is not None:
		st.write(f"정답 단어 카테고리: {tc.get('target_word_category')}")
	if tc.get("questions", None) is not None:
		st.write(tc.get("questions"))
		

