from src.Controllers import init_state
from src.route import route
from src.Views.Components import Sidebar

def preprocess():
    init_state()

def init():
    preprocess()
    Sidebar.render()
    route(Sidebar.get_selected_page())

__all__ = [
    "init"
]