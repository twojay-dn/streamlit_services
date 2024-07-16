from src.Views.Components import render_page, BaseTabs, BaseColumns
from src.Views.Pages.Sections.Quiz_sections import init, chat_part
import streamlit as st

@render_page(name="Quiz")
def page():
    tabs = BaseColumns([
        lambda: init(need_base_controller=True),
        chat_part,
	])
    tabs.render()