import json

def read_file(file_path : str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def read_json(file_path : str) -> dict:
  with open(file_path, "r") as file:
    return json.load(file)