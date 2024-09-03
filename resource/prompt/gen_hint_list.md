generate {count} hints about {target_word} for the guessing game. You will write {count} of hints for {target_word}.

## Ordering
- First, write the most important hint.
- Second, write the second most important hint.
- Third, write the third most important hint.
- And so on.

Each hint should be more clear and significant than the previous one.

## Constraints
- Do not notify or say the answer word in your response directly.
- {target_word} is the answer. So you must hide the answer in your all responses.
- Your hints are not allowed to be the same.
- Your hints must be related to {target_word}. Use words and expressions that are related to {target_word}.
- Your response should understandable for early students of an elementary school. the text should be contains word and expressions in 800 of the Lexile Rating.
- Each hint should be very short and concise, within 14 words.
- Enclose each hint in double quotes.
- If you're need to write {target_word}, you must write this as "this".
- When creating hints, arrange them in a clear order from first to last, with the correct answer. The clearer the answer, the later it should be.
- Just write each hint in a sentence.

## Format
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
```
{"properties": {"hints": {"description": "List of hints", "items": {"type": "string"}, "title": "Hints", "type": "array"}}, "required": ["hints"]}
```