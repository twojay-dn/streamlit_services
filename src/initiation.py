from src.Controllers import BaseController
from src.route import route
from src.Views.Components import Sidebar
import os

def preprocess():
    BaseController.set_state("check", 42)
    from dotenv import load_dotenv
    load_dotenv()

def init():
    preprocess()
    Sidebar.render()
    route(Sidebar.get_selected_page())

__all__ = [
    "init"
]