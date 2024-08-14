generate "[count]" questions about "[target_word]" of "[target_category]" for the guessing game.

each question is within 7 words. and all of questions is understandable and easy to answer for kindergarten students. So, you must use simple and easy words.

### Constraints
- "[target_word]" is the answer. So you must hide the answer in your questions. Do not contain the answer word in generated questions.
- Your questions are not allowed to be the same.
- Your questions must be related to "[target_word]" and "[target_category]". Use words and expressions that are related to that.
- Your response should contains understandable and enough easy questions for kindergarten students.
- Your questions should be easy to answer.

### Ordering
- When creating questions, arrange them in a clear order from first to last, with the correct answer. The clearer the answer, the later it should be. It means, the clearer the answer, the index of the question should be bigger.
- do not use bullet points or other formatting. Just write the questions in a list.

### Format
- Enclose each question in double quotes.
- The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"questions": {"description": "List of [count] questions in total", "items": {"type": "string"}, "title": "Questions", "t   ype": "array"}}, "required": ["questions"]}
```