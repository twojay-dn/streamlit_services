import os, csv, shutil, json, random
import dotenv

dotenv.load_dotenv()

def read_file(path: str) -> str:
  with open(path, "r", encoding="utf-8") as f:
    return f.read()

def read_csv(path: str) -> list[str]:
  with open(path, "r", encoding="utf-8") as f:

    reader = csv.reader(f)
    next(reader)
    return [tuple(row) for row in reader]
  
def log(sentence: str, verbose: bool):
  if verbose:
    print(sentence)

from openai import OpenAI

def openai_api_request(system_prompt: str = None, user_prompt: str = None):
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  messages = [
  ]
  if system_prompt:
    messages.append({"role": "system", "content": system_prompt})
  if user_prompt:
    messages.append({"role": "user", "content": user_prompt})
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": system_prompt}
    ]
  )
  return response.choices[0].message.content

def write_file(path: str, data: str):
  with open(path, "a", encoding="utf-8") as f:  # "w" 대신 "a" 모드 사용
    f.write(data + "\n")  # 각 데이터 뒤에 새 줄 추가

def main(n: int, verbose: bool):
  prompt = read_file(f"{os.getcwd()}/prompt/gen_hint_list.md")
  wordpool = read_csv(f"{os.getcwd()}/words.csv")
  result_path = f"{os.getcwd()}/result"
  if not os.path.exists(result_path):
    os.makedirs(result_path)
  else:
    shutil.rmtree(result_path)
    os.makedirs(result_path)

  sampled = random.sample(wordpool, n)
  for i in range(n):
    log(f"Running case {i+1}/{n}", verbose)
    log(f"word: {sampled[i]}", verbose)
    target_word = sampled[i][0]
    count = 11
    system_prompt = str(prompt).replace("{target_word}", target_word)
    system_prompt = system_prompt.replace("{count}", str(count))
    res = openai_api_request(system_prompt)
    log(res, verbose)
    write_file(f"{result_path}/result.md", f"Answer word : {target_word} =============")
    write_file(f"{result_path}/result.md", res)


if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("--n", help="number of running cases", type=int, required=True, default=1)
  parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, required=True)
  args = parser.parse_args()
  main(args.n, args.verbose)