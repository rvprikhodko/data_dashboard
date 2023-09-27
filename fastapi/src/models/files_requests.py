from sqlalchemy import Column, Integer, String, Date, Boolean
from src.models.base import Base


class FilesRequests(Base):
    __tablename__ = 'files_requests'
    id = Column(Integer, primary_key=True)
    upload = Column(Boolean)
    download = Column(Boolean)
    get_columns = Column(Boolean)
    task_type = Column(String, nullable=True)
    model_type = Column(String, nullable=True)
    done_by = Column(Integer, nullable=True)
    done_at = Column(Date, nullable=True)
