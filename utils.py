import csv, os

def load_wordpool():
  path = f"{os.getcwd()}/resource/words.csv"
  with open(path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    wordpool = [tuple(row) for row in reader]
  return wordpool

def load_prompt(prompt_name : str):
  path = f"{os.getcwd()}/resource/prompt/{prompt_name}.md"
  with open(path, "r", encoding="utf-8") as f:
    return f.read()