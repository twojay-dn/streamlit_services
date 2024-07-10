import streamlit as st
from src.Views.Components import render_page, BaseColumns

@render_page(name="Generation")
def page():
    st.text_input("enter the answer")
    st.button("Generate")
    
    def hints_dashboard():
        st.write("Hints")
        st.write("Hints")
        st.write("Hints")
        st.write("Hints")
        st.write("Hints")
    
    def questions_dashboard():
        st.write("Questions")
        st.write("Questions")
        st.write("Questions")
        st.write("Questions")
        st.write("Questions")
    
    cols = BaseColumns([hints_dashboard, questions_dashboard])
    cols.render()
