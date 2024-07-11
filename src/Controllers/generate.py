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

def inference_generation_questions(answer : str = "", count : int = 0, model_name : str = "gpt-3.5-turbo") -> List[str]:
    parser =  JsonOutputParser(pydantic_object=QuestionList)
    prompt = PromptTemplate.from_template(
        get_questions_gen_prompt()
    )
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=0.7,
        top_p=0.95
    )
    chain = prompt | llm | parser
    return chain.invoke({
        "quiz_answer": answer, 
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
        temperature=0.7,
        top_p=0.95
    )
    chain = prompt | llm | parser
    return chain.invoke({
        "quiz_answer": answer, 
        "count": count, 
        "format_instructions": parser.get_format_instructions()
    })

__all__ = ["inference_generation_questions", "inference_generation_hints"]