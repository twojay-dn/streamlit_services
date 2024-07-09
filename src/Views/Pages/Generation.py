import streamlit as st
from src.Views.Components import render_page, BaseColumns

@render_page(name="Generation")
def page():
    st.text_input("enter the answer")
    st.button("Generate")
    
    def first_col():
        st.write("This is the first column")
    
    def second_col():
        st.write("This is the second column")
    
    cols = BaseColumns([first_col, second_col])
    cols.render()
