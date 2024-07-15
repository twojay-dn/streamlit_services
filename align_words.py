import pandas as pd

# CSV 파일 읽기
import os
file_path = f'{os.getcwd()}/resource/words.csv'  # 여기에 CSV 파일 경로를 입력하세요
df = pd.read_csv(file_path)

# 정렬할 열의 이름 (예: 'name')
column_to_sort_by = 'word'  # 여기에 정렬할 열 이름을 입력하세요

# 중복된 단어 제거
df = df.drop_duplicates(subset=[column_to_sort_by])

# 특정 열을 기준으로 알파벳 정렬
df_sorted = df.sort_values(by=column_to_sort_by, ascending=True)

# 정렬된 데이터프레임 출력
print(df_sorted)

# 정렬된 결과를 새로운 CSV 파일로 저장
sorted_file_path = f'{os.getcwd()}/resource/sorted_words.csv'  # 여기에 저장할 파일 경로를 입력하세요
df_sorted.to_csv(sorted_file_path, index=False)