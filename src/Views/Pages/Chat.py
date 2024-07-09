import streamlit as st
from src.Controllers import BaseController
from src.Views.Components import render_page, ChatBoxComponent
from src.Controllers.ChatMemory import MemoryController
from src.Controllers.LLM import OpenAIController

@render_page(name="Chat")
def page():
    st.write(BaseController.get_state("check"))
    
    memory=MemoryController()
    llm=OpenAIController("gpt-3.5-turbo")
    chatbox = ChatBoxComponent(memory=memory, llm=llm)
    chatbox.render()
    