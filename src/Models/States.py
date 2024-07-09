import streamlit as st
from typing import Any

class State:
    @staticmethod
    def get(key : str, value : Any = None) -> Any:
        if key not in st.session_state:
            st.session_state[key] = value
        return st.session_state[key]
    
    @staticmethod
    def set(key : str, value : Any):
        st.session_state[key] = value