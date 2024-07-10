generate {count} questions about {quiz_answer} for the guessing game.

for example, if the quiz answer is "apple", the questions could be "What is the color of this?", "What is the shape of this?", "What is the taste of this?"

### constraints
- {quiz_answer} is the answer. So you must hide the answer in your questions.
- Your questions are not allowed to be the same.
- Your questions must be related to {quiz_answer}. Use words and expressions that are related to {quiz_answer}.
- Your questions should understandable for early students of an elementary school.

### ordering
질문을 생성할 때, 첫 질문부터 마지막 질문까지 명확한 순서대로 정렬하세요.

- You must use the following format:
    - question 1
    - question 2
    - ...
    - question {count}

- do not use bullet points or other formatting. Just write the questions in a list.

{format_instructions}