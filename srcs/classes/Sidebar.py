import streamlit as st
from Enums import views_list_as_str

sidebar_title = "AI Test Generation"
page_selectbox_label = "Select a page"

class Sidebar:
    @classmethod
    def render(cls):
        st.sidebar.title(sidebar_title)
        cls.selected_view = st.sidebar.selectbox(
            page_selectbox_label,
            views_list_as_str
        )
    
    @classmethod
    def get_selected_view(cls):
        return cls.selected_view