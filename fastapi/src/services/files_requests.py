from datetime import datetime
from typing import List
from fastapi import Depends

from sqlalchemy.orm import Session

from src.db.db import get_session

from src.models.files_requests import FilesRequests


class FilesRequestsService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add(self,
            upload: bool, download: bool, get_columns: bool, task_type: str, model_type: str, cur_used_id: int):
        requests_schema = {}
        requests_schema['upload'] = upload
        requests_schema['download'] = download
        requests_schema['get_columns'] = get_columns
        requests_schema['task_type'] = task_type
        requests_schema['model_type'] = model_type
        requests_schema['done_at'] = datetime.now()
        requests_schema['done_by'] = cur_used_id
        requests_schema_packed = FilesRequests(**requests_schema)
        self.session.add(requests_schema_packed)
        self.session.commit()

    def get(self, request_id: int) -> FilesRequests:
        request = (
            self.session
            .query(FilesRequests)
            .filter(
                FilesRequests.id == request_id,
            )
            .first()
        )
        return request

    def all(self) -> List[FilesRequests]:
        requests = (
            self.session
            .query(FilesRequests)
            .order_by(
                FilesRequests.id.desc()
            )
            .all()
        )
        return requests

