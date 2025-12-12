from pydantic import BaseModel
from pydantic_config_generator import prompt, write_ini, ENVIRON_MODE_SKIP


class Circle(BaseModel):
    radius: float
    border_color: str
    fill_color: str = '#FF0000'
    text: str = None
    shadow: bool = False
    

config = prompt(Circle, environ_mode=ENVIRON_MODE_SKIP)
print(config)

write_ini(config)
