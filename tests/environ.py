from pydantic import BaseModel
from pydantic_config_generator import prompt, write_ini


class Circle(BaseModel):
    radius: float
    border_color: str
    fill_color: str = '#FF0000'
    text: str = None
    

config = prompt(Circle, environ_as_default=True)
print(config)

write_ini(config)
