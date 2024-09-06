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

### Examples
- this is cases that user's answer is right

<answer_word>egg</answer_word>
<user_input>egg</user_input>
>> assistant : 1

<answer_word>fruit</answer_word>
<user_input>is that fruit?</user_input>
>> assistant : 1

<answer_word>light</answer_word>
<user_input>is that a light?</user_input>
>> assistant : 1

<answer_word>eraser</answer_word>
<user_input>is that an eraser?</user_input>
>> assistant : 1

<answer_word>cat</answer_word>
<user_input>Is it a cat?</user_input>
>> assistant : 1

- this is cases that user's answer is wrong

<answer_word>sad</answer_word>
<user_input>Is the word happy?</user_input>
>> assistant : 0

<answer_word>jump</answer_word>
<user_input>run</user_input>
>> assistant : 0

<answer_word>bag</answer_word>
<user_input>Is it a cap?</user_input>
>> assistant : 0

<answer_word>giraffe</answer_word>
<user_input>Is that a zebra?</user_input>
>> assistant : 0

<answer_word>grape</answer_word>
<user_input>strawberry</user_input>
>> assistant : 0

## output
- response should be formatted as json
```
{
  "reasoning" : "reasoning for the result",
  "result" : 1 or 0
}
```
