Judge user's answer is right or wrong. this instruction has three conditions to judge

1. The user is clearly and unambiguously referring to <answer_word>.
2. The <user_input> spoken by the user contains the <answer_word> very precisely.
3. The user is clearly confident in the correct answer and submitting it.

- If the user is asking a general question about an object that could be related to the answer word, but is not specifically about the answer word, the result should be 0.

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

<answer_word>bag</answer_word>
<user_input>bag?</user_input>
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
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"reasoning": {"description": "reasoning for the result", "type": "string"}, "result": {"description": "1 or 0", "type": "integer"}}, "required": ["reasoning", "result"]}
```