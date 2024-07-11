from langchain_openai import ChatOpenAI
from openai import OpenAI
from src.utils import get_api_key
from abc import ABC, abstractmethod
from typing import Literal, Callable, Any, List
from src.Controllers.ChatMemory import BaseMemoryController
import types
import streamlit as st
import os
import inspect

def validate_params(required : List[str] = []):
    def decorator(func):
        def wrapper(*args, **kwargs):
            inference_callback = args[1]  # 첫 번째 인자는 self, 두 번째 인자가 inference_callback
            sig = inspect.signature(inference_callback)
            for param in required:
                if param not in sig.parameters:
                    raise ValueError(f"inference_callback must have a '{param}' parameter")
            return func(*args, **kwargs)
        return wrapper
    return decorator

class BaseLLMController(ABC):
    def __init__(self, model : str, api_key : str = None):
        self.model = model
        if api_key is None:
            self.api_key = get_api_key()
        else:
            self.api_key = api_key
        
    @abstractmethod
    def inference(self, prompt : str, memory : BaseMemoryController):
        pass
    
    @validate_params(required = ["self", "prompt"])
    def overwrite_call_to_inference(self, inference_callback : Callable):
        assert isinstance(inference_callback, types.FunctionType), "inference must be a function"
        self.inference = types.MethodType(inference_callback, self)

class OpenAIController(BaseLLMController):
    def __init__(self, model : str, api_key : str = None):
        super().__init__(model, api_key)
        self.client = OpenAI(api_key=self.api_key)
    
    
    def inference(self, prompt : str, messages : BaseMemoryController):
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
    
    def inference(self, prompt : str, messages : BaseMemoryController):
        self.client.invoke(messages)

class HyperParameter:
    def __init__(self, **kwargs):
        self.hyperparameters = kwargs
        
    def get(self, key : str, default : Any = None):
        return self.hyperparameters[key]

    def set(self, key : str, value : Any):
        self.hyperparameters[key] = value
        
    def unpack(self):
        return self.hyperparameters