import streamlit as st
from default_value import config

from sidebar import sidebar
from hints import hints
from quiz import quiz

state_manager = st.session_state

def main():
	st.set_page_config(layout="wide")
	sidebar(component=st.sidebar, state_manager=state_manager)
	tab1, tab2 = st.tabs(["힌트 질문 생성", "챗봇"])
	with tab1:
		hints(component=st, state_manager=state_manager)
	with tab2:
		quiz()

if __name__ == "__main__":
	main()