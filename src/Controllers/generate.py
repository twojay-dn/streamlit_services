from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from src.utils import load_prompt_from_name, get_api_key
import streamlit as st

api_key = get_api_key()
questions_gen_prompt = load_prompt_from_name("questions_generation_prompt")
hints_gen_prompt = load_prompt_from_name("hints_generation_prompt")

def generate_questions(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt = PromptTemplate.from_template(questions_gen_prompt)
    formatted_prompt = prompt.format(answer=answer, count=count)
    llm = OpenAI(model=model_name, api_key=api_key)
    chain = formatted_prompt | llm
    return chain.invoke({"answer": answer, "count": count})

def generate_hints(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt = PromptTemplate.from_template(hints_gen_prompt)
    formatted_prompt = prompt.format(answer=answer, count=count)
    llm = OpenAI(model=model_name, api_key=api_key)
    chain = formatted_prompt | llm
    return chain.invoke({"answer": answer, "count": count})

__all__ = ["generate_questions", "generate_hints"]