import random
import streamlit as st
from .shared import dream_image_key, dalle_drawing_style_code, resources_path, prompt_path, image_generation_parameter
from openai import OpenAI
from utils import read_file
import os
import json

output_form = """
- The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema(do not use backticks for the schema):
{
  "prompt" : {
    "title" : "prompt",
    "description" : "a prompt to draw a dream in a style of {style_name}.",
    "type" : "string"
  }
}
"""

def generate_prompt_Dalle(dream_info : str, style_name : str):
  client = OpenAI()
  system_prompt = read_file(f"{prompt_path}/dream_drawing_prompt_making.md")
  system_prompt.format(user_dream_information=dream_info, style_name=style_name, ratio=image_generation_parameter["ratio"], format_instruction=output_form)
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": system_prompt}
    ]
  )

  return json.loads(response.choices[0].message.content)

def generate_image_Dalle(prompt : str):
  client = OpenAI()
  response = client.images.generate(
    prompt=prompt,
    n=1,
    size=image_generation_parameter["size"]
  )
  return response.data[0].url

# 여러스타일로 많이? 단일 스타일로?
def dream_image():
  if st.session_state.get(dream_image_key) is None:
    st.error("꿈 내용을 아직 알 수 없습니다.")
    return
  
  dream_info = st.session_state.get(dream_image_key)
  st.write("꿈 이미지 기반 Dalle 프롬프트")
  
  for _ in range(4):
    style = random.choice(dalle_drawing_style_code)
    st.write(f"스타일 : {style}")
    prompt = generate_prompt_Dalle(dream_info, style)
    st.write(prompt)
    image_url = generate_image_Dalle(prompt)
    st.image(image_url)