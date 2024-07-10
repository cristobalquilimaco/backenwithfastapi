from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    age: int