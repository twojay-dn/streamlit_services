import streamlit as st

class Refresher:
  @staticmethod
  def run(postprocessed_data):
    st.write(postprocessed_data)
    return postprocessed_data
