from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.orm import Session
from src.core.settings import settings
from src.db.db import get_session
from src.models.schemas.utils.jwt_token import JwtToken
from src.models.schemas.users.users_request import UsersRequest
from src.models.users import Users


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/users/authorize')


def get_current_user_id(token: str = Depends(oauth2_schema)) -> int:
    return UserService.verify_token(token)


class UserService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def check_password(password_text: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hash)

    @staticmethod
    def create_token(user_id: int) -> JwtToken:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': str(user_id),
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')

        return payload.get('sub')

    def register(self, user_schema: UsersRequest, cur_user_id: get_current_user_id) -> None:
        user_schema_unpacked = user_schema.dict()
        user_schema_unpacked['password_hashed'] = self.hash_password(user_schema.password_text)
        del user_schema_unpacked['password_text']
        user_schema_unpacked['created_at'] = datetime.now()
        user_schema_unpacked['created_by'] = cur_user_id
        user_schema_unpacked['modified_at'] = datetime.now()
        user_schema_unpacked['modified_by'] = cur_user_id
        user = Users(**user_schema_unpacked)
        self.session.add(user)
        self.session.commit()

    def register_init(self, user_schema: dict) -> None:
        user_schema_unpacked = user_schema
        user_schema_unpacked['password_hashed'] = self.hash_password(user_schema['password_text'])
        del user_schema_unpacked['password_text']
        user_schema_unpacked['created_at'] = datetime.now()
        user_schema_unpacked['created_by'] = 0
        user_schema_unpacked['modified_at'] = datetime.now()
        user_schema_unpacked['modified_by'] = 0
        user = Users(**user_schema_unpacked)
        self.session.add(user)
        self.session.commit()

    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
            .query(Users)
            .filter(Users.username == username)
            .first()
        )

        if not user:
            return None
        if not self.check_password(password_text, user.password_hashed):
            return None

        return self.create_token(user.id)

    def get(self, users_id: int) -> Users:
        user = (
            self.session
            .query(Users)
            .filter(
                Users.id == users_id,
            )
            .first()
        )
        return user

    def all(self) -> List[Users]:
        users = (
            self.session
            .query(Users)
            .order_by(
                Users.id.desc()
            )
            .all()
        )
        return users

    def add(self, users_schema: UsersRequest, cur_user_id: int) -> Users:
        users_schema_unpacked = users_schema.dict()
        users_schema_unpacked['password_hashed'] = self.hash_password(users_schema_unpacked['password_text'])
        del users_schema_unpacked['password_text']
        users_schema_unpacked['created_at'] = datetime.now()
        users_schema_unpacked['created_by'] = cur_user_id
        users_schema_unpacked['modified_at'] = datetime.now()
        users_schema_unpacked['modified_by'] = cur_user_id
        user = Users(**users_schema_unpacked)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, users_schema: UsersRequest, cur_user_id: int) -> Users:
        user = self.get(user_id)
        for field, value in users_schema:
            setattr(user, field, value)
        setattr(user, 'created_by', user.created_by)
        setattr(user, 'created_at', user.created_at)
        setattr(user, 'modified_by', cur_user_id)
        setattr(user, 'modified_at', datetime.now())
        self.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()
