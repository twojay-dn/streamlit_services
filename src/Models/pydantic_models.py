from pydantic import BaseModel, Field
from typing import List

class Config(BaseModel):
    model_config = {
        "title" : "Config"
    }
    
class HintList(BaseModel):
    hints : List[str] = Field(description="List of hints")

class QuestionList(BaseModel):
    questions : List[str] = Field(description="List of questions")
