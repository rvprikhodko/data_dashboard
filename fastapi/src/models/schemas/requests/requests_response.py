from pydantic import BaseModel
from datetime import date


class RequestsResponse(BaseModel):
    id: int
    type: str
    column: str
    response: int
    done_by: date
    done_at: int

    class Config:
        orm_mode = True
