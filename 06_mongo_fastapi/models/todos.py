from pydantic import BaseModel

class Todo(BaseModel):
    name:str
    descrption:str
    completed:bool