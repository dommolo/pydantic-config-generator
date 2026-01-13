from pydantic import BaseModel
from pydantic_config_generator import prompt, write_ini, ENVIRON_MODE_SKIP, DEFAULT_MODE_AUTO


class Line(BaseModel):
    color: str
    width: int = 1


class Circle(BaseModel):
    radius: float
    border_color: str
    fill_color: str = '#FF0000'
    text: str = None
    shadow: bool = False
    border: Line
    

config = prompt(Circle, environ_mode=ENVIRON_MODE_SKIP, default_mode=DEFAULT_MODE_AUTO)
print(config)

write_ini(config)
