from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str = 'localhost'
    port: int = 9999
    connection_string: str = 'postgresql://postgres:Aa229400@localhost:5432/FP'
    jwt_expires_seconds: int = 3600
    jwt_secret: str = 'MyBigSecret'
    jwt_algorithm: str = 'HS512'
    admin_username: str = 'admin'
    admin_password: str = 'admin'


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8',
)
