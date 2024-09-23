import streamlit as st
from typing import List, Dict, Any
import csv, os, random, json, time
from openai import OpenAI
from collections import Counter
from static_messages import *

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def init():
    st.session_state.setdefault("words", read_csv(f"{os.getcwd()}/resource/words.csv"))
    st.session_state.setdefault("test_results", [])

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def read_csv(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        next(reader)  # 첫 줄(헤더) 건너뛰기
        return list(reader)

def generate_hint(target_word: str, target_category: str, count: int = 11) -> List[str]:
    target_word = target_word.lower()
    target_category = target_category.lower()
    prompt = read_file(f"{os.getcwd()}/resource/prompt/gen_hint_list.md")
    prompt = prompt.replace("{target_word}", target_word)
    prompt = prompt.replace("{target_category}", target_category)
    prompt = prompt.replace("{count}", str(count))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
        ],
        temperature=0.56,
        max_tokens=1200,
        top_p= 1
    )
    content = response.choices[0].message.content
    if "```" in content:
        content = content.replace("```json","").replace("```","")
    result_list = json.loads(content)["hints"]
    return result_list

def save_results_to_csv(results: List[Dict[str, Any]], filename: str):
    keys = results[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

def main():
    st.title("프롬프트 테스트 애플리케이션")

    test_mode = st.radio("테스트 모드 선택", ["랜덤 테스트", "사용자 입력 테스트"])

    num_tests = st.number_input("테스트 횟수를 입력하세요:", min_value=1, max_value=100, value=10)

    if test_mode == "사용자 입력 테스트":
        target_word = st.text_input("테스트할 단어를 입력하세요:")
        target_category = st.text_input("테스트할 카테고리를 입력하세요:")

    if st.button("테스트 시작"):
        progress_bar = st.progress(0)
        results = []

        for i in range(num_tests):
            if test_mode == "랜덤 테스트":
                random_word = random.choice(st.session_state.words)
                target_word = random_word['word']
                target_category = random_word['category']

            start_time = time.time()
            hints = generate_hint(target_word, target_category)
            end_time = time.time()

            results.append({
                "test_number": i + 1,
                "target_word": target_word,
                "target_category": target_category,
                "hints": hints,
                "time_taken": end_time - start_time
            })

            progress_bar.progress((i + 1) / num_tests)

        st.session_state.test_results = results
        st.rerun()

    if st.session_state.test_results:
        st.write("테스트 결과:")
        for result in st.session_state.test_results:
            st.write(f"테스트 #{result['test_number']}")
            st.write(f"대상 단어: {result['target_word']}")
            st.write(f"카테고리: {result['target_category']}")
            st.write(f"소요 시간: {result['time_taken']:.2f}초")
            st.write("생성된 힌트:")
            for hint in result['hints']:
                st.write(f"- {hint}")
            st.write("---")

        st.write("모든 테스트가 완료되었습니다.")

        if st.button("결과 저장"):
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"test_results_{timestamp}.csv"
            save_results_to_csv(st.session_state.test_results, filename)
            st.success(f"결과가 {filename}에 저장되었습니다.")

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    init()
    main()
