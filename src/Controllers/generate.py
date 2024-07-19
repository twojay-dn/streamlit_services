from typing import List
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from src.utils import load_prompt_from_name, get_api_key
from src.Models.pydantic_models import QuestionList, HintList
import streamlit as st

api_key = get_api_key()

@st.cache_data
def get_questions_gen_prompt():
    return load_prompt_from_name("questions_generation_prompt")

@st.cache_data
def get_hints_gen_prompt():
    return load_prompt_from_name("hints_generation_prompt")

def get_prompt(key : str = ""):
    return load_prompt_from_name(key)

def inference_generation_list(key : str = "", target_word : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    prompt_text = get_prompt(key)
    parser =  JsonOutputParser(pydantic_object=QuestionList)
    prompt = PromptTemplate.from_template(
        prompt_text
    )
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.65,
    )
    chain = prompt | llm | parser
    return chain.invoke({
        "quiz_category": target_word, 
        "count": count, 
        "format_instructions": parser.get_format_instructions()
    })

def inference_generation_questions(target_word : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    parser =  JsonOutputParser(pydantic_object=QuestionList)
    prompt = PromptTemplate.from_template(
        get_questions_gen_prompt()
    )
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.65,
        max_tokens=500,
    )
    chain = prompt | llm | parser
    return chain.invoke({
        "quiz_category": target_word, 
        "count": count, 
        "format_instructions": parser.get_format_instructions()
    })

def inference_generation_hints(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    parser =  JsonOutputParser(pydantic_object=HintList)
    prompt = PromptTemplate.from_template(
        get_hints_gen_prompt()
    )
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.65,
    )
    chain = prompt | llm | parser
    return chain.invoke({
        "quiz_answer": answer, 
        "count": count, 
        "format_instructions": parser.get_format_instructions()
    })

__all__ = ["inference_generation_questions", "inference_generation_hints"]