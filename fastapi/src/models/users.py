from sqlalchemy import Column, Integer, String, Date
from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hashed = Column(String)
    role = Column(String)
    created_at = Column(Date, nullable=True)
    created_by = Column(Integer, nullable=True)
    modified_at = Column(Date, nullable=True)
    modified_by = Column(Integer, nullable=True)