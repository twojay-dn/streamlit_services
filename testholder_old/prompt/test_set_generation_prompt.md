첨부하는 words.csv의 word 카테고리 내의 단어들을 answer_word로 사용하여, 아래의 예시를 참고하여 데이터를 생성하세요.

-----------------
Please create a test set in CSV format that meets the requirements below.

### tags

- The CSV file that is generated should start with the categories below.

answer_word, user_input, label, result

### Data specification and its contents

- answer_word : The word here means the correct word for the quiz. There is one or two words in English.
- user_input : The sentence spoken by the user.
- label : 1 if the user's answer is correct, 0 if the user's answer is incorrect.
- result : the result will be written after the test. so, keep it blank.

this is a situation where the user doesn't know the answer, and the answer is correct if the user says it.

the conditions to judge the user's answer are as follows.
1. The user is clearly and unambiguously referring to <answer_word>.
2. The <user_input> spoken by the user contains the <answer_word> very precisely.
3. The user is clearly confident in the correct answer and submitting it with certainty as <answer_word>.

#### test-set for right answer

The test set for the right answer satisfies all of the following characteristics
- The user_input clearly contains the <answer_word>
- The user is clear and confident about the <answer_word> and submits it
- The user submits the correct answer with certainty. Exclude cases where there is no certainty.

#### test-set for wrong answer

A dataset for a wrong answer has the opposite characteristics of a dataset for a right answer.
A test set for a wrong answer satisfies one or more of the following characteristics
- The <user_input> does not contain and apears the <answer_word>
- The user is unclear about the <answer_word> or just speculates it.
- The user does not submit the correct answer as <answer_word>.
- The user talks about something unrelated to <answer_word> or submits the wrong word.