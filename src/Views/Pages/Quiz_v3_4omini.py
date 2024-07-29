from src.Views.Components import render_page, BaseTabs, BaseColumns
from src.Views.Pages.Sections.Quiz_sections3_4omini import generation_column, chat_column
import streamlit as st

@render_page(name="Quiz_v3_4omini")
def page():
    tabs = BaseColumns([
        generation_column,
        chat_column,
	])
    tabs.render()