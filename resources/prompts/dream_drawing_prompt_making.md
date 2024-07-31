make a prompt to draw user's dream in a style of <style_name>.

### Dream Information
Here is the user's dream:
<user_dream_information>.

### Drawing Style
- Make a prompt to draw a dream in a style of <style_name>.

### Output Format
Write a prompt to draw a dream in a style of <style_name>.
```
"[target_object], [target_place], [target_description] in a <style_name> style, ratio of <ratio>"
```
insert certaing information to the prompt, especially target_object, target_place, and target_description.

target_object, target_place, and target_description can be extracted from the user's dream.

### Output
- Response in English
- Response in 400 words or less
- The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {{"foo": ["bar", "baz"]}} is a well-formatted instance of the schema. The object {{"properties": {{"foo": ["bar", "baz"]}}}} is not well-formatted.

Here is the output schema:
```json
{
	"prompt" : {
		"title" : "prompt",
		"description" : "a prompt to draw a dream in a style of <style_name>.",
		"type" : "string"
	}
}
```