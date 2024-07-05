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
        response = self.model.chat.completions.create(
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
        
    def inference(self, message):
        self.messages.append({'role': 'agent', 'content': message})
        response = self.model.inference(self.messages, parameters=self.parameters)
        self.messages.append({'role': 'user', 'content': response})
        return response

class End_condition:
    def __init__(self, limit_turn : int = None, soft_condition_prompt : str = None):
        assert limit_turn is not None or soft_condition_prompt is not None, "Either limit_turn or soft_condition_prompt must be provided"
        self.limit_turn = limit_turn
        self.soft_condition_prompt = soft_condition_prompt

    def check(self, messages : Messages):
        turn = messages.get_turn_count()
        if self.limit_turn and turn > self.limit_turn:
            return True
        if self.soft_condition_prompt:
            return self.soft_condition_prompt.check(messages)
        return False

class Table:
    def __init__(self) -> None:
        self.table = []
        self.end_condition = End_condition()

    def save_dialogue_history_as_file(self, filepath):
        self.dialogue_history.save_as_file(filepath)

    def sit(self, agent: Agent):
        self.table.append(agent)

    def leave(self, agent: Agent):
        self.table.remove(agent)

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