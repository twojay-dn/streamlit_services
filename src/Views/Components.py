import streamlit as st
from src.Views import View_pages

title_description = "Sidebar"
page_choise_description = "Sidebar"

class Sidebar:
    name = title_description
    
    @classmethod
    def render(cls):        
        st.sidebar.title(cls.name)
        cls.page = st.sidebar.selectbox(
            page_choise_description, 
            options=View_pages.get_view_list(retrieve_value=True), 
            index=0
        )
        
    @classmethod
    def get_selected_page(cls):
        return cls.page