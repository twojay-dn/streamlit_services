import streamlit as st
from dotenv import load_dotenv
from classes.Sidebar import Sidebar
from classes.State import State
from classes.WordsPool import WordsPool
from views import Chat, TestGeneration

def pre_init():
    load_dotenv()
    WordsPool.init()
    State.init({
        "check" : 42
    })

def init():
    pre_init()
    Sidebar.render()

    choosen = Sidebar.get_selected_view()
    if choosen == "Chat":
        Chat.render()
    else:
        TestGeneration.render()