from pydantic import BaseModel


class UsersRequest(BaseModel):
    username: str
    password_text: str
    role: str

