import random
import streamlit as st
from .shared import *
from openai import OpenAI
from utils import get_system_prompt, insert_parameters
import json
from .shared import prompt_path
from classes.llm import Retrier, CONDITION_FORMAT

dalle_client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY"))

def generate_prompt_Dalle(dream_info : json, style_name : str):
	client = OpenAI()
	system_prompt = get_system_prompt(f"{prompt_path}/dream_drawing_prompt_making.md")
	system_prompt = insert_parameters(system_prompt, {
		"user_dream_information" : str(dream_info),
		"style_name" : style_name,
		"ratio" : image_generation_parameter["ratio"]
	})
	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": system_prompt}
		],
		temperature=0.7
	)
	return response.choices[0].message.content



def generate_image_Dalle(prompt : str, n : int = 1, size : str = "1024x1024"):
	response = dalle_client.images.generate(
		prompt=prompt,
		n=n,
		size=size
	)
	return response.data[0].url

def call_to_generate_image(prompt : str):
	return generate_image_Dalle(prompt)

@Retrier.retry_on_invalid_response(
	max_tries=3,
	condition_format=CONDITION_FORMAT.JSON
)
def call_to_generate_dalle_prompt(dream_info : json, style_name : str):
	return generate_prompt_Dalle(dream_info, style_name)

# 여러스타일로 많이? 단일 스타일로?
def dream_image():
	if st.session_state.get(dream_image_key) is None:
		st.error("꿈 내용을 아직 알 수 없습니다.")
		return
	
	dream_info : json = st.session_state.get(dream_image_key)
	st.write("꿈 이미지 기반 Dalle 프롬프트")
	
	st.session_state[images_list_key] = []
	for _ in range(4):
		style = random.choice(dalle_drawing_style_code)
		st.write(f"스타일 : {style}")
		prompt : json = call_to_generate_dalle_prompt(dream_info, style)
		st.write(f"생성 결과물 : {prompt}")
		st.write(f"프롬프트 텍스트 : {prompt.get('prompt')}")
		image_url : str = call_to_generate_image(prompt.get("prompt"))
		st.image(image_url)
		st.session_state[images_list_key].append(image_url)