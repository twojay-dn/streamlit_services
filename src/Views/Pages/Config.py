import streamlit as st
from src.Controllers import BaseController
from src.Controllers.LLM import HyperParameter
from src.Views.Components import render_page, BaseColumns
from src.utils import load_default_config_json

@render_page(name="Config")
def page():
    st.write("This is the config view")
    
    input_data = load_default_config_json()
    BaseController.set_state("params", HyperParameter(**input_data), overwrite=False)
    hyper_params = BaseController.get_state("params")

    def config_panel():
        temperature = st.slider(
            label="temperature", 
            min_value=0.0, 
            max_value=1.0, 
            step=0.1, 
            value=hyper_params.get("temperature", 0.5),
        )
        hyper_params.set("temperature", temperature)
            
    def config_dashboard():
        st.write(hyper_params.unpack())
    
    config_columns = BaseColumns(
        column_callbacks=[config_panel, config_dashboard],
        widths=[1, 3]
    )
    config_columns.render()    