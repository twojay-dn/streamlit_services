import streamlit as st
from typing import Any

class State:
    @staticmethod
    def get(key : str or int, value : Any = None) -> Any:
        if key not in st.session_state:
            st.session_state[key] = value
        return st.session_state[key]
    
    @staticmethod
    def set(key : str or int, value : Any):
        st.session_state[key] = value
        
    @staticmethod
    def delete(key : str or int):
        if key in st.session_state:
            del st.session_state[key]