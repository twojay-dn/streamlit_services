
import sys, os, csv, json, random, shutil
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except IOError:
        print(f"오류: '{file_path}' 파일을 읽는 중 문제가 발생했습니다.")
        sys.exit(1)

def read_csv(path: str) -> list[str]:
  with open(path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    return [tuple(row) for row in reader]

log_path = f"{os.getcwd()}/log"

def log(sentence: str, verbose: bool, written_log: bool):
  if verbose:
    print(sentence)
  if written_log:
    write_file(f"{log_path}/log.md", sentence)

def write_file(path: str, data: str):
  with open(path, "a", encoding="utf-8") as f:
    f.write(data + "\n")

def openai_api_request(system_prompt: str = None, user_prompt: str = None):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": system_prompt}
    ]
  )
  return response.choices[0].message.content

def main(n: int, verbose: bool, written_log : bool):
  file_path = f'{os.getcwd()}/resource/prompt/gkp_target_word.md'
  system_prompt = read_file(file_path)
  wordpool = read_csv(f"{os.getcwd()}/resource/words.csv")
  sampled = random.sample(wordpool, n)
  count = 15
  
  if not os.path.exists(log_path):
    os.makedirs(log_path)
  else:
    shutil.rmtree(log_path)
    os.makedirs(log_path)
  
  for i in range(n):
    target_word, target_category = sampled[i]
    temp_system_prompt = str(system_prompt).replace("{count}", str(count))
    temp_system_prompt = temp_system_prompt.replace("{target_word}", target_word)
    temp_system_prompt = temp_system_prompt.replace("{target_category}", target_category)
    res = openai_api_request(temp_system_prompt)
    log(f"Running case {i+1}/{n} ============ target_word: {target_word} | {target_category} ====", verbose, written_log)
    log(res, verbose, written_log)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, required=True)
    parser.add_argument("--log", action=argparse.BooleanOptionalAction, required=True)
    args = parser.parse_args()
    main(args.n, args.verbose, args.log)