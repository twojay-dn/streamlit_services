from src.Controllers import BaseController
from src.route import route
from src.Views.Components import Sidebar
from src.utils import load_json
import streamlit as st

def preprocess():
	st.set_page_config(layout="wide")
	metadata = load_json("resource/metadata.json")
	BaseController.set("supported_models", metadata["supported_models"])
	static_messages = load_json("resource/static_messages.json")
	BaseController.set("welcome_messages", static_messages["welcome"])
	BaseController.set("correct_messages", static_messages["correct"])

def init():
	preprocess()
	Sidebar.render()
	route(Sidebar.get_selected_page())

__all__ = [
	"init"
]