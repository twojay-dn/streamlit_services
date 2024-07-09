from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from src.utils import load_prompt_from_name
import streamlit as st
import os

if os.getenv("RUN_ENV").lower() == "local":
    api_key = os.getenv("OPENAI_API_KEY")
elif os.getenv("RUN_ENV").lower() == "production":
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    raise ValueError("RUN_ENV must be 'local' or 'production' to use OpenAI")

questions_gen_prompt = load_prompt_from_name("questions_generation_prompt")
hints_gen_prompt = load_prompt_from_name("hints_generation_prompt")

def generation_questions(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt = PromptTemplate.from_template(questions_gen_prompt)
    formatted_prompt = prompt.format(answer=answer, count=count)  # 수정된 부분
    llm = OpenAI(model=model_name, api_key=api_key)
    chain = formatted_prompt | llm  # 수정된 부분
    return chain.invoke({"answer": answer, "count": count})

def generation_hints(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt = PromptTemplate.from_template(hints_gen_prompt)
    formatted_prompt = prompt.format(answer=answer, count=count)  # 수정된 부분
    llm = OpenAI(model=model_name, api_key=api_key)
    chain = formatted_prompt | llm  # 수정된 부분
    return chain.invoke({"answer": answer, "count": count})