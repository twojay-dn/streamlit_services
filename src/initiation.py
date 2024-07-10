from src.Controllers import BaseController
from src.route import route
from src.Views.Components import Sidebar
import os
from src.utils import load_json
import streamlit as st

def preprocess():
    st.set_page_config(layout="centered")
    from dotenv import load_dotenv
    load_dotenv()
    
    metadata = load_json("resource/metadata.json")
    BaseController.set_state("supported_models", metadata["supported_models"])

def init():
    preprocess()
    Sidebar.render()
    route(Sidebar.get_selected_page())

__all__ = [
    "init"
]