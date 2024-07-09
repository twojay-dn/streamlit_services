import streamlit as st
from typing import Callable

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
        assert callable(func), "Function is required"
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = BasePage(name, description)
            page.render(func)
        return wrapper
    return decorator