from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.models.schemas.users.users_request import UsersRequest
from src.models.schemas.users.users_response import UsersResponse
from src.services.users import UserService
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.users import get_current_user_id

from src.core.settings import settings

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация')
def register(user_schema: UsersRequest, users_service: UserService = Depends(),
             user_id: int = Depends(get_current_user_id)):
    print(user_id)
    return users_service.register(user_schema, user_id)


@router.post('/authorize', response_model=JwtToken, name='Авторизация')
def authorize(auth_schema: OAuth2PasswordRequestForm = Depends(), users_service: UserService = Depends()):
    # users = users_service.all()
    # admin_bool = False
    # for user in users:
    #     if user.username == 'admin':
    #         admin_bool = True
    #         break
    # if not admin_bool:
    #     admin_schema = {
    #         "username": settings.admin_username,
    #         "password_text": settings.admin_password,
    #         "role": "admin"
    #     }
    #     users_service.register_init(admin_schema)
    result = users_service.authorize(auth_schema.username, auth_schema.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован')
    return result


@router.get('/all', response_model=List[UsersResponse], name='Получить всех пользователей')
def all(users_service: UserService = Depends(), user_id: int = Depends(get_current_user_id)):
    user = users_service.get(user_id)
    if user.role != 'admin':
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    return users_service.all()


@router.get('/get/{user_id}', response_model=UsersResponse, name='Получить одного пользователя')
def get(user_id: int, users_service: UserService = Depends(), cur_user_id: int = Depends(get_current_user_id)):
    user = users_service.get(cur_user_id)
    if user.role != 'admin':
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    return get_with_check(user_id, users_service)


def get_with_check(user_id: int, users_service: UserService):
    result = users_service.get(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')
    return result


@router.post('/', response_model=UsersResponse, status_code=status.HTTP_201_CREATED, name='Добавить пользователя')
def add(user_schema: UsersRequest, users_service: UserService = Depends(),
        user_id: int = Depends(get_current_user_id)):
    user = users_service.get(user_id)
    if user.role != 'admin':
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    return users_service.add(user_schema, user_id)


@router.put('/{user_id}', response_model=UsersResponse, name='Обновить информацию о пользователе')
def put(user_id: int, user_schema: UsersRequest, user_service: UserService = Depends(),
        cur_user_id: int = Depends(get_current_user_id)):
    user = user_service.get(cur_user_id)
    if user.role != 'admin':
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    get_with_check(user_id, user_service)
    return user_service.update(user_id, user_schema, cur_user_id)


@router.delete('/{users_id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя')
def delete(user_id: int, user_service: UserService = Depends(),
           cur_user_id: int = Depends(get_current_user_id)):
    user = user_service.get(cur_user_id)
    if user.role != 'admin':
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    get_with_check(user_id, user_service)
    return user_service.delete(user_id)
