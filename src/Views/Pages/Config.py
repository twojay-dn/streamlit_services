import streamlit as st
from src.Controllers import BaseController
from src.Controllers.LLM import HyperParameter
from src.Views.Components import render_page, BaseColumns, slider, number_inputbox, VerticalColumns
from src.utils import load_default_config_json

@render_page(name="Config")
def page():
    input_data = load_default_config_json()
    BaseController.set("params", HyperParameter(**input_data), overwrite=False)
    hyper_params = BaseController.get("params")

    def config_panel():
        slider("temperature", float(0.0), float(1.0), float(0.1), float(hyper_params.get("temperature", 0.5)))
        # slider("top_p", float(0.0), float(1.0), float(0.01), float(hyper_params.get("top_p", 0.9)))
        slider("frequency_penalty", float(-2.0), float(2.0), float(0.1), float(hyper_params.get("frequency_penalty", 0.0)))
        slider("presence_penalty", float(-2.0), float(2.0), float(0.1), float(hyper_params.get("presence_penalty", 0.0)))
        number_inputbox("max_tokens", 1, 1000, 10, hyper_params.get("max_tokens", 100))
    
    def model_selection():
        st.write("Model Selection")
        st.selectbox("Model", BaseController.get("supported_models"))
    
    def config_dashboard():
        st.write(hyper_params.unpack())
    vc = VerticalColumns(column_callbacks=[model_selection, config_dashboard])

    config_columns = BaseColumns(
        column_callbacks=[config_panel, vc.render],
        widths=[1, 3]
    )
    config_columns.render()

