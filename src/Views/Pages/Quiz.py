from src.Views.Components import render_page, BaseTabs
from src.Views.Pages.Sections.Quiz_sections import init, chat_part

@render_page(name="Quiz")
def page():
	tabs = BaseTabs([
		("Init", lambda: init(need_base_controller=True)),
		("Chat", chat_part)
	])
	tabs.render()