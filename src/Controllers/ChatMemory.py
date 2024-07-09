import streamlit as st
import os

from typing import Dict, List
from abc import ABC, abstractmethod
from langchain_community.chat_message_histories import StreamlitChatMessageHistory, ChatMessageHistory
from langchain_openai import ChatOpenAI

class BaseMemoryController(ABC):
    def __init__(self, limit_turn : int = 200):
        self.memory = []
        self.limit_length = limit_turn * 2

    @abstractmethod
    def add_message(self, message : Dict[str, str]) -> None:
        pass
    
    @abstractmethod
    def get_memory(self):
        pass

class MemoryController(BaseMemoryController):
    def __init__(self, limit_turn : int = 200):
        self.memory = []
        self.limit_length = limit_turn * 2

    def add_message(self, message : Dict[str, str]) -> None:
        if len(self.memory) >= self.limit_length:
            self.memory = self.memory[2:]
        self.memory.append(message)

    def get_memory(self) -> List[Dict[str, str]]:
        return self.memory

class LangchainMemoryController(BaseMemoryController):
    def __init__(self, limit_turn : int = 200):
        self.limit_length = limit_turn * 2
        if os.getenv("RUN_ENV").lower() == "local":
            self.memory = ChatMessageHistory()
        elif os.getenv("RUN_ENV").lower() == "production":
            self.memory = StreamlitChatMessageHistory(key="chat_history")
        else:
            raise ValueError("RUN_ENV must be 'local' or 'production' to use LangchainMemoryController")

        
    def add_message(self, message : Dict[str, str]) -> None:
        if message["role"] == "user":
            self.memory.add_user_message(message["content"])
        else:
            self.memory.add_ai_message(message["content"])
            
    def get_memory(self) -> List[Dict[str, str]]:
        return self.memory