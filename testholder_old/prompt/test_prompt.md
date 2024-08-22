Judge user's answer is right or wrong. this instruction has three conditions to judge

1. The user is clearly and unambiguously referring to <answer_word>.
2. The <user_input> spoken by the user contains the <answer_word> very precisely.
3. The user is clearly confident in the correct answer and submitting it.

### input data

a user message would contain <answer_word> and <user_input> tags. check both of them and judge whether the user's answer is right or wrong.
- <answer_word> is usually a single word, but it can be multiple words. In this case, you need to make sure it contains all of those words.
- <user_input> is a sentence spoken by the user.

#### input_format
<answer_word></answer_word>
<user_input></user_input>

### output
- just answer with 1 or 0 with no additional text. If all conditions are satisfied, answer 1. Otherwise, answer 0.

### Examples
- this is cases that user's answer is right
{{few_shots_right}}

- this is cases that user's answer is wrong
{{few_shots_wrong}}