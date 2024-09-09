generate {count} hints about {target_word} for the guessing game. You will write {count} of hints for {target_word}.

## Ordering
- First, write the most important and clear hint.
- Second, write the second most important hint.
- Third, write the third most important hint.
- And so on.

Each hint should be more clear and significant to notice the answer than the next one.

## Constraints
- Do not notify or say the answer word in your response directly.
- {target_word} is the answer. So you must hide the answer in your all responses. Do not contain the answer : {target_word} in your hints in any case.
- Your hints are not allowed to be the same.
- Your hints must be related to {target_word}. Use words and expressions that are related to {target_word}.
- Your response should understandable for kindergarten students. the text should be contains word and expressions for kindergarten students.
- Each hint should be very short and concise. write each hint in 10 words or less.
- Enclose each hint in double quotes write each hint in a sentence format of python.
- If you're need to write {target_word}, you must write this as "this" or "it" or other pronoun.
- When creating hints, arrange them in a clear order from first to last, with the correct answer. The clearer the answer, the later it should be.


## Format
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of  strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"hints": {"description": "List of hints", "items": {"type": "string"}, "title": "Hints", "type": "array"}}, "required": ["hints"]}
```