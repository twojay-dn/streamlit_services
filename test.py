import openai

openai.api_key = 'sk-proj-LVd3cN5RvmJ74y3QFyOJT3BlbkFJ2z3AekICFT3Ekb2sERi3'

response = openai.chat.completions.create(
    n=4,
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': '안녕하세요! 최근에 꾼 꿈에 대해 이야기해 주실 수 있나요? 언제 그 꿈을 꾸었는지 궁금합니다.'}]
)

print(response)