import streamlit as st
from src.Controllers import BaseController
from src.Views.Components import render_page, ChatBoxComponent, BaseTabs
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController
from src.Views.Pages.Sections.Quiz_hint import generate_hints, generate_questions

# TODO : 이 안에서 퀴즈 구성에 필요한 플로우 구성해서 진행할 것
def print_llm_state(self, prompt, memory):
    return "hello override"

def chat_part():
    BaseController.set_state("memory", MemoryController())
    llm = OpenAIController("gpt-3.5-turbo")
    llm.overwrite_call_to_inference(print_llm_state)
    BaseController.set_state("llm", llm)
    chatbox = ChatBoxComponent(
        memory=BaseController.get_state("memory"),
        llm=BaseController.get_state("llm")
    )
    chatbox.render()

@render_page(name="Quiz")
def page():
    tabs = BaseTabs([
        ("Generate Hints", generate_hints),
        ("Generate Questions", generate_questions),
        ("Chat", chat_part)
    ])
    tabs.render()