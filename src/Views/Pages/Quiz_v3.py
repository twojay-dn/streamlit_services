from src.Views.Components import render_page, BaseColumns
from src.Views.Pages.Sections.Quiz_sections3 import generation_column, chat_column

@render_page(name="Quiz_v3")
def page():
  tabs = BaseColumns([
    generation_column,
    chat_column,
	])
  tabs.render()