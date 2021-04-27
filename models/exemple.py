from pydantic import BaseModel


class MyModel(BaseModel):
    id: int
    value: int