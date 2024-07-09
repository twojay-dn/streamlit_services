from pydantic import BaseModel

class Config(BaseModel):
    model_config = {
        "title" : "Config"
    }