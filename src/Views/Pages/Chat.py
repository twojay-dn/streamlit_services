import streamlit as st
from src.Controllers import BaseController
from src.Views.Components import render_page, ChatBoxComponent
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController

@render_page(name="Chat")
def page():
    st.write(BaseController.get_state("check"))
    
    BaseController.set_state("memory", MemoryController(), overwrite=False)
    BaseController.set_state("llm", OpenAIController("gpt-3.5-turbo"), overwrite=False)
    chatbox = ChatBoxComponent(
        memory=BaseController.get_state("memory"),
        llm=BaseController.get_state("llm")
    )
    chatbox.render()