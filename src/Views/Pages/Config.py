import streamlit as st
from src.Controllers import BaseController
from src.Controllers.LLM import HyperParameter
from src.Views.Components import render_page
from src.utils import load_default_config_json

@render_page(name="Config")
def page():
    st.write("This is the config view")
    
    input_data = load_default_config_json()
    BaseController.set_state("params", HyperParameter(**input_data), overwrite=False)
    hyper_params = BaseController.get_state("params")
    st.write(hyper_params.unpack())