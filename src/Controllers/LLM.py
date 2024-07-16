from langchain_openai import ChatOpenAI
from openai import OpenAI
from src.utils import get_api_key
from abc import ABC, abstractmethod
from typing import Callable, Any, List
from src.Controllers.ChatMemory import BaseMemoryController
import types
from src.utils import validate_function_params, load_prompt_from_name


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
	
	@validate_function_params(required = ["self", "prompt", "memory"])
	def overwrite_call_to_inference(self, inference_callback : Callable):
		assert isinstance(inference_callback, types.FunctionType), "inference must be a function"
		self.inference = types.MethodType(inference_callback, self)

class OpenAIController(BaseLLMController):
	def __init__(self, model : str, api_key : str = None, sysprompt_key : str = None):
		super().__init__(model, api_key)
		self.client = OpenAI(api_key=self.api_key)
		if sysprompt_key is not None:
			self.system_prompt = load_prompt_from_name(sysprompt_key)
    
	def inference(self, prompt : str, messages : BaseMemoryController):
		if messages is None:
			raise ValueError("messages is None")
		messages = messages.get_memory()
		if self.system_prompt is not None:
			messages = [{"role": "system", "content": self.system_prompt}] + messages
		response = self.client.chat.completions.create(
			model=self.model,
			messages=messages
		)
		response = response.choices[0].message.content
		return response
	
	def set_system_prompt(self, sysprompt_path : str):
		with open(sysprompt_path, "r") as file:
			self.sysprompt = file.read()

	def insert_prompt_parameters(self, parameters : dict):
		for key, value in parameters.items():
			if key not in self.system_prompt:
				raise ValueError(f"Key {key} is not in the system prompt")
			self.system_prompt = self.system_prompt.replace(f"{key}", value)

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