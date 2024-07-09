import os, json

def get_absolute_path(path : str) -> str:
    return os.path.abspath(path)

def read_file(path : str) -> str:
    with open(path, "r") as file:
        return file.read()
    
def read_json_file(path : str) -> dict:
    with open(path, "r") as file:
        return json.load(file)