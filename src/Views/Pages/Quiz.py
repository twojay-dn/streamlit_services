import streamlit as st
from src.Controllers import BaseController
from src.Views.Components import render_page, ChatBoxComponent, BaseTabs
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController
from src.Views.Pages.Sections.Quiz_hint import generate_hints, generate_questions

def chat_part():
    BaseController.set_state("memory", MemoryController())
    BaseController.set_state("llm", OpenAIController("gpt-3.5-turbo"))
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