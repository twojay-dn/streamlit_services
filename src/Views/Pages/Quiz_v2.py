from src.Views.Components import render_page, BaseTabs, BaseColumns
from src.Views.Pages.Sections.Quiz_sections3 import generation_column, chat_column
import streamlit as st

@render_page(name="Quiz_v2")
def page():
    tabs = BaseColumns([
        generation_column,
        chat_column,
	])
    tabs.render()