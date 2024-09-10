import os, json, shutil, csv
from openai import OpenAI

def read_file(path: str) -> str:
  with open(path, "r") as f:
    return f.read()
  
def write_file(path: str, content: str):
  with open(path, "w") as f:
    f.write(content)
    
def refresh_folder(path: str):
  if os.path.exists(path):
    shutil.rmtree(path)
  os.makedirs(path)

def main(n: int):
  client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", type=int, required=True)
  args = parser.parse_args()
  main(args.n)
