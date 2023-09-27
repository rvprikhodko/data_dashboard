from pydantic import BaseModel


class RequestsRequest(BaseModel):
    type: str
    column: str
    response: str
