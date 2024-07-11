generate {count} questions about {quiz_answer} for the guessing game.

for example, if the quiz answer is "apple", the questions could be "What is the color of this?", "What is the shape of this?", "What is the taste of this?"

### Constraints
- {quiz_answer} is the answer. So you must hide the answer in your questions.
- Your questions are not allowed to be the same.
- Your questions must be related to {quiz_answer}. Use words and expressions that are related to {quiz_answer}.
- Your questions should understandable for early students of an elementary school.

### Ordering
When creating questions, arrange them in a clear order from first to last, with the correct answer. The clearer the answer, the later it should be.

- You must use the following format as list:
[
    hint 1,
    hint 2,
    ...,
    hint {count},
]

- do not use bullet points or other formatting. Just write the questions in a list.

### Format
{format_instructions}