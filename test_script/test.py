
from openai import OpenAI
from dotenv import load_dotenv
import json, shutil, os, csv, random

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  

def generate_llm_response(prompt, model_name, hyper_params, user_input_message):
  response = client.chat.completions.create(
    model=model_name,
    messages=[
      {"role": "system", "content": prompt},
      {"role": "user", "content": user_input_message}
    ],
    **hyper_params
  )
  return response.choices[0].message.content


def make_user_input_message(query, answer_word):
  return f"""
<answer_word>{answer_word}</answer_word>
<user_input>{query}</user_input>
"""

def inference(prompt, model_name, hyper_params, query, answer_word):
  prompt = str(prompt)
  user_input_message = make_user_input_message(query, answer_word)
  response = generate_llm_response(prompt, model_name, hyper_params, user_input_message)
  return response


def read_file(path):
  with open(path, "r") as f:
    return f.read()

def write_file(path, content):
  with open(path, "w") as f:
    f.write(content)

def read_json(path):
  with open(path, "r") as f:
    return json.load(f)

def read_csv(path):
  with open(path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # 헤더 건너뛰기
    return [tuple(row) for row in reader]


dataset_path = f"{os.getcwd()}/resource/dataset"
dataset_list = os.listdir(dataset_path)
def read_dataset(file_path):
  dataset = []
  with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
      line = line.strip()
      if line:
        try:
          data = json.loads(line)
          dataset.append(data)
        except json.JSONDecodeError:
          print(f"잘못된 JSON 형식: {line}")
  return dataset

def main(n):
  result_dir = f"{os.getcwd()}/result"
  shutil.rmtree(result_dir, ignore_errors=True)
  os.makedirs(result_dir, exist_ok=True)
  
  result_path = f"{result_dir}/result.md"
  prompt_path = f"{os.getcwd()}/resource/prompt/check_answer_in_query.md"
  config_path = f"{os.getcwd()}/config.json"
  words_path = f"{os.getcwd()}/resource/words.csv"
  words = read_csv(words_path)
  dataset_path = f"{os.getcwd()}/resource/dataset"
  dataset_list = os.listdir(dataset_path)
  
  result = {}
  for dataset_name in dataset_list:
    key = dataset_name.split(".")[0]
    dataset_path = f"{os.getcwd()}/resource/dataset/{dataset_name}"
    dataset = read_dataset(dataset_path)
    result[key] = dataset
  print(result)
  
  
  for i in range(n):
    key = random.choice(list(result.keys()))
    dataset = result[key]
    res = ""
  for key, dataset in result.items():
    prompt = read_file(prompt_path)
    config = read_json(config_path)
    model_name = config["model_name"]
    hyper_params = config["hyper_params"]
    for query in dataset:
      res += f"=================== {key} : {query['content']} =============\n"
      res += inference(prompt, model_name, hyper_params, query["content"], key)
      res += "\n\n"
  write_file(result_path, res)
  
if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", type=int, default=10)
  args = parser.parse_args()
  main(args.n)
