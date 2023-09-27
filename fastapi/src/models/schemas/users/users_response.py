from pydantic import BaseModel
from datetime import date


class UsersResponse(BaseModel):
    id: int
    username: str
    password_hashed: str
    role: str
    created_at: date
    created_by: int
    modified_at: date
    modified_by: int

    class Config:
        orm_mode = True
