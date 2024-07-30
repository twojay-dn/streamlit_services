import streamlit as st
from typing import Any

class State:
  @staticmethod
  def get(key: str, value: Any = None) -> Any:
    if key not in st.session_state:
      if value is not None:
        st.session_state[key] = value
        return value
      else:
        return None
    return st.session_state[key]
  
  @staticmethod
  def set(key: str, value: Any, overwrite: bool = True) -> None:
    if overwrite or key not in st.session_state:
      st.session_state[key] = value
