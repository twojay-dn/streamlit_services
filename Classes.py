from openai import OpenAI
import os
from typing import List, Dict, Any

class Messages:
    def __init__(self):
        self.history = []
        self.turn_count = 0
        
    def save_as_file(self, filepath):
        with open(filepath, 'w') as file:
            for dialogue in self.history:
                file.write(f"{dialogue['role']}: {dialogue['content']}\n")
            
    def append(self, role, content):
        self.history.append({'role': role, 'content': content})

    def get_history(self):
        return self.history
    
    def get_turn_count(self):
        return self.turn_count
    
    def clear(self):
        self.history = []

class Model:
    def __init__(self):
        self.model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_callsign = "gpt-4o"

    def inference(self, messages : List[Dict[str, str]], parameters: Dict[str, Any] = None):
        if parameters is None:
            parameters = {
                "model": self.model_callsign,
                "messages": messages,
            }
        else:
            parameters = {
                "model": self.model_callsign,
                "messages": messages,
                **parameters
            }
        response = self.chat.completions.create.create(
            **parameters
        )
        return response.choices[0].message.content

class Agent:
    def __init__(self, name, description, parameters : Dict[str, Any] = None):
        self.name = name
        self.description = description
        self.model = Model()
        self.parameters = parameters
        self.messages = Messages()
        
    def inference(self, message) -> str:
        if message is not None:
            self.messages.append(self.name, message)
        response = self.model.inference(self.messages, parameters=self.parameters)
        self.messages.append(self.name, response)
        return response

def merge_messages(messages_a : Messages, messages_b : Messages, is_a_assistant : bool = True) -> Messages:
    merged_messages = Messages()
    array = enumerate(zip(messages_a.get_history(),messages_b.get_history()))
    if is_a_assistant:
        for i, (a,b) in array:
            if i % 2 == 0:
                merged_messages.append("assistant", a['content'])
            else:
                merged_messages.append("user", b['content'])
    else:
        for i, (a,b) in array:
            if i % 2 == 0:
                merged_messages.append("user", b['content'])
            else:
                merged_messages.append("assistant", a['content'])
    return merged_messages