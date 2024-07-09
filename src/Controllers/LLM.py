from langchain_openai import ChatOpenAI
from openai import OpenAI
from abc import ABC, abstractmethod
from typing import Literal, Callable
from src.Controllers.ChatMemory import BaseMemoryController
import types
import streamlit as st
import os

def _get_api_key():
    run_env = os.getenv("RUN_ENV")
    match run_env:
        case "local":
            return os.getenv("OPENAI_API_KEY")
        case "production":
            return st.secrets["OPENAI_API_KEY"]
        case _:
            raise ValueError(f"RUN_ENV must be set to 'local' or 'production' : {run_env}")
        
class BaseLLMController(ABC):
    def __init__(self, model : str, api_key : str = None):
        self.model = model
        if api_key is None:
            self.api_key = _get_api_key()
        else:
            self.api_key = api_key
        
    def inference(self, prompt : str):
        response = self.inference(prompt)
        return response
    
    def overwrite_call_to_inference(self, inference : Callable):
        assert isinstance(inference, types.FunctionType), "inference must be a function"
        self.inference = types.MethodType(inference, self)
        
class OpenAIController(BaseLLMController):
    def __init__(self, model : str, api_key : str = None):
        super().__init__(model, api_key)
        self.client = OpenAI(api_key=self.api_key)
    
    def inference(self, role : Literal["user", "assistant"], prompt : str, messages : BaseMemoryController):
        messages = messages.get_memory()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        response = response.choices[0].message.content
        return response

class LangchainOpenaiController(BaseLLMController):
    def __init__(self, model : str, api_key : str = None):
        super().__init__(model, api_key)
        self.client = ChatOpenAI(model=model, api_key=self.api_key)
    
    def inference(self, role : Literal["user", "assistant"], prompt : str, messages : BaseMemoryController):
        self.client.invoke(messages)
        