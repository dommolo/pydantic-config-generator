from pydantic import BaseModel
from pydantic_config_generator import prompt, write_ini, write_env


class Test(BaseModel):
    primo: int
    terzo: int = 0
    quarto: int = None
    sesto: str
    ottavo: str = 'test'
    nono: str = None
    
    
    
fields = Test.__fields__.items()

for key, field in fields:
    print(f'{key}: required={field.required}, allow_none={field.allow_none}, default={field.default}, type={field.type_}')

config = prompt(Test)