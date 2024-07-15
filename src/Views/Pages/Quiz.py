import streamlit as st
from src.Controllers import BaseController
from src.Views.Components import render_page, ChatBoxComponent, BaseTabs
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController
from src.Views.Pages.Sections.Quiz_sections import init, chat_part

@render_page(name="Quiz")
def page():
    tabs = BaseTabs([
        ("Init", init),
        ("Chat", chat_part)
    ])
    tabs.render()