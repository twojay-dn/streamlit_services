generate {count} hints about {target_word} for the guessing game. You will write {count} of hints for {target_word}.

## Ordering
- First, write the most important and clear hint.
- Second, write the second most important hint.
- Third, write the third most important hint.
- And so on.

Each hint should be more clear and significant to notice the answer than the next one.
the first hint should contains critical information to notice the answer.
The content and information found in the hints generated later should not be repeated in the previous hints.

## Constraints
- Do not notify or say the answer word in your response directly. never use the word : {target_word} in any case of your response.
- Your hints are not allowed to be the same. Your hints must be related to {target_word}. Use words and expressions that are related to {target_word}.
- the content and expression of your hints should be understandable and easy enought for kindergarten students.
- Each hint should be very short and concise. write each hint in 8 words or less.
- If you're need to write {target_word}, you must write this as "this" or "it" or other pronoun.
- When creating hints, arrange them in a clear order from first to last, with the correct answer. The clearer the answer, the later it should be.


## Format
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of  strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Do not expose the schema directly.
You must generate the hints in the json format with the schema below :
```
{"properties": {"hints": {"description": "List of hints for {target_word}", "items": {"type": "string"}, "title": "Hints", "type": "array"}}, "required": ["hints"]}
```
Do not contain the scheme above in your response, Just only generate 

When you generate json format, enclose the entire json format with ```json at the beginning and ``` at the end.

Enclose each hint in double quotes. Do not use '"\"' in your hints. just one double quote mark for each hint.
