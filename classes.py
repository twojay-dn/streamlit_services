from typing import Dict, Any

class Data:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def reset_boolean_values(self):
        for key, value in self.data.items():
            if isinstance(value, bool):
                self.data[key] = False

    def get(self, key: str):
        return self.data[key]
    
    def set(self, key: str, value: Any):
        self.data[key] = value

    def get_data(self):
        return self.data
    
    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return self.data
    
class ChatMemory:
    def __init__(self):
        self.memory = []

    def add_message(self, role : str, content : str):
        self.memory.append({
            "role" : role,
            "content" : content
        })
    
    def get_messages(self):
        return self.memory