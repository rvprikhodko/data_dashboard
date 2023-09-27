from fastapi import FastAPI
from src.api.base_router import router


tags_dict = [

]

app = FastAPI(
    title='Мини-проект с FastAPI',
    description='Работа с подключением БД',
    version='0.0.1',
    openapi_tags=tags_dict
)

app.include_router(router)