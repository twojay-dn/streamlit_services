import streamlit as st
from typing import Any, Dict

class State:
    @staticmethod
    def init(params : Dict[str, Any]):
        for key, value in params.items():
            st.session_state[key] = value

    @staticmethod
    def get(key : str, value : Any = None) -> Any:
        if key not in st.session_state:
            st.session_state[key] = value
        return st.session_state[key]
    
    @staticmethod
    def set(key : str, value : Any):
        st.session_state[key] = value