import os, json

def read_file(file_path):
  with open(file_path, "r") as file:
    return file.read()

prompts_path = f"{os.getcwd()}/resource/prompts"

def read_prompt(prompt_name : str, file_ext : str = "md"):
  if prompt_name not in os.listdir(prompts_path):
    raise ValueError(f"Prompt {prompt_name}.{file_ext} not found. Check your file and try again.")
  return read_file(f"{prompts_path}/{prompt_name}.{file_ext}")

__all__ = [
  "read_file"
]