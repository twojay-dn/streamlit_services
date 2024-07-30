import streamlit as st
from langchain.memory import ConversationBufferMemory

class Memory(ConversationBufferMemory):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.memory_key = "chat_history"
    
  def add_user_message(self, input_message : str, output_message : str):
    self.save_context(
      inputs={"human": input_message},
      outputs={"ai": output_message}
    )
  def load_memory(self):
    return self.load_memory_variables({})
