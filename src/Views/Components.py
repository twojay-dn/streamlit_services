import streamlit as st
from typing import Callable, Literal, List

title_description = "Sidebar"
page_choise_description = "Sidebar"

class Sidebar:
    name = title_description
    
    @classmethod
    def render(cls):
        from src.Views import View_pages
       
        st.sidebar.title(cls.name)
        cls.page = st.sidebar.selectbox(
            page_choise_description,
            options=View_pages.get_view_list(retrieve_value=True), 
            index=0
        )
        
    @classmethod
    def get_selected_page(cls):
        return cls.page

class BaseColumns:
    def __init__(self,
            column_callbacks : List[Callable] = None,
            gap : Literal["small", "medium", "large"] = "small",
        ):
        if column_callbacks is None:
            column_callbacks = []
        if not all(isinstance(column_callback, Callable) for column_callback in column_callbacks):
            raise ValueError("All column_callbacks must be callable")
        self.col_len = len(column_callbacks)
        self.columns = enumerate(column_callbacks)
        self.gap = gap

    def add_column(self, column_callback : Callable):
        if not isinstance(column_callback, Callable):
            raise ValueError("column_callback must be a callable")
        self.columns.append(column_callback)
        self.col_len = len(self.columns)

    def render(self):
        col_list = st.columns(
            self.col_len,
            gap = self.gap
        )
        for index, column_callback in self.columns:
            with col_list[index]:
                column_callback()

class BasePage:
    def __init__(self, name : str, description : str = None):
        self.name = name
        self.description = description
        
    def render(self, impl_callback : Callable):
        st.title(self.name)
        if self.description is not None:
            st.subheader(self.description)
        impl_callback()

from functools import wraps
def render_page(name: str, description: str = None):
    def decorator(func):
        assert name is not None, "Name is required"
        assert hasattr(func, '__call__'), "Function is required"
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = BasePage(name, description)
            page.render(func)
        return wrapper
    return decorator

from src.Controllers.ChatMemory import BaseMemoryController
from src.Controllers.LLM import BaseLLMController

# class BaseChatBox:
#     def __init__(self, memory : BaseMemoryController, llm : BaseLLMController):
#         self.memory = memory
#         self.llm = llm
        
#     def render(self):
#         st.chat_input("Enter your message")
#         st.chat_message("user").write(st.session_state.message)
        
#     def call_inference(self):
#         pass
    
class ChatBoxComponent:
    def __init__(self, memory : BaseMemoryController, llm : BaseLLMController):
        self.memory = memory
        self.llm = llm    