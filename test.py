from pydantic import BaseModel
from pydic import run

class ExampleSubConfig(BaseModel):
    name: str
    surname: str
    age: int

class ExampleConfig(BaseModel):
    name: str = ''
    surname: str
    age: int
    is_student: bool = True
    teacher: ExampleSubConfig = None

run(ExampleConfig)
