import streamlit as st

def render():
    st.title("Hint Generation")
    st.write("This is the hint generation view")
    
    st.text_input("enter the answer")
    st.button("Generate")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("This is the first column")
    with col2:
        st.write("This is the second column")