import os, json
from typing import List

def load_file(path : str) -> str:
    with open(path, "r") as file:
        return file.read()

def load_json(path : str) -> dict:
    with open(path, "r") as file:
        return json.load(file)
