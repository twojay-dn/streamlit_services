from enum import Enum

class LLM_VENDOR(Enum):
  OPENAI = "openai"
  
  def get_needed_parameters(self):
    if self == LLM_VENDOR.OPENAI:
      return ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"]
    else:
      raise ValueError(f"Unsupported LLM vendor: {self}")

class LLM_MODEL(Enum):
  GPT_4O = ("GPT-4", "gpt-4o", LLM_VENDOR.OPENAI)
  GPT_3_5_TURBO = ("GPT-3.5 Turbo", "gpt-3.5-turbo", LLM_VENDOR.OPENAI)

  def __init__(self, model_name, model_id, vendor):
    self.model_name = model_name
    self.model_id = model_id
    self.vendor = vendor

  @classmethod
  def get_model_list(cls):
    return [model for model in cls]

  @classmethod
  def get_vendor(cls, model_name):
    for model in cls:
      if model.model_name == model_name:
        return model.vendor
    return None