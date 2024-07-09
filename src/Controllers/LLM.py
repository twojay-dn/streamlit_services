from langchain_core.chat_models import ChatOpenAI
from openai import OpenAI
from abc import ABC, abstractmethod
from typing import Literal
import types

class BaseLLMController(ABC):
    def __init__(self, model : str, api_key : str):
        self.model = model
        self.api_key = api_key
        
    def inference(self, prompt : str):
        response = self.inference(prompt)
        return response
    
    def overwrite_call_to_inference(self, inference : Callable):
        assert isinstance(inference, types.FunctionType), "inference must be a function"
        self.inference = types.MethodType(inference, self)
        
class OpenAIController(BaseLLMController):
    def __init__(self, model : str, api_key : str):
        super().__init__(model, api_key)
        self.client = OpenAI(api_key=api_key)
    
    def inference(self, role : Literal["user", "assistant"], prompt : str, messages : BaseChatController):
        messages = messages.get_messages()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response})
        return response

class LangchainOpenaiController(BaseLLMController):
    def __init__(self, model : str, api_key : str):
        super().__init__(model, api_key)
        self.client = ChatOpenAI(model=model, api_key=api_key)
    
    def inference(self, role : Literal["user", "assistant"], prompt : str, messages : BaseChatController):
        self.client.invoke(messages)
        