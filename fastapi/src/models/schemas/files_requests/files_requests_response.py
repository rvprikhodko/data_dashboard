from pydantic import BaseModel
from datetime import date


class RequestsResponse(BaseModel):
    id: int
    upload: bool
    download: bool
    get_columns: bool
    task_type: str
    model_type: str
    done_at: date
    done_by: int

    class Config:
        orm_mode = True
