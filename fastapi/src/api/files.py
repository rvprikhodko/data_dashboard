from fastapi import APIRouter, BackgroundTasks, UploadFile, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, HTMLResponse, PlainTextResponse
from src.models.schemas.files_requests.files_requests_response import RequestsResponse
from src.services.files_requests import FilesRequestsService
from src.services.users import UserService, get_current_user_id
from typing import List

from src.services.files import FilesService

router = APIRouter(
    prefix='/files',
    tags=['files'],
)


@router.get('/all', response_model=List[RequestsResponse], name='Все запросы с csv файлами')
def all(requests_service: FilesRequestsService = Depends(), users_service: UserService = Depends(),
        user_id: int = Depends(get_current_user_id)):
    # user = users_service.get(user_id)
    # if user.role != 'admin':
    #     return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Нет доступа')
    return requests_service.all()


@router.post('/upload', name='Загрузить файл для предобработки')
def upload(background_tasks: BackgroundTasks, file: UploadFile, files_service: FilesService = Depends(),
           requests_service: FilesRequestsService = Depends(), users_service: UserService = Depends(),
           ):
    # user_id = get_current_user_id()
    requests_service.add(upload=True, download=False, get_columns=False, task_type='None', model_type='None',
                         cur_used_id=-1)
    background_tasks.add_task(files_service.data_preprocessing, file.file)


@router.get('/df', name='Получить датафрейм (для dash)')
def get_df(files_service: FilesService = Depends(),
           requests_service: FilesRequestsService = Depends(),
           users_service: UserService = Depends(),
           ):
    # user_id = get_current_user_id()
    requests_service.add(upload=False, download=False, get_columns=False, task_type='get_df', model_type='get_df',
                         cur_used_id=-1)

    return files_service.return_df()


@router.get('/download', name='Скачаль файл с предобработанными данными')
def download(files_service: FilesService = Depends(),
             requests_service: FilesRequestsService = Depends(),
             users_service: UserService = Depends(),
             ):
    # user_id = get_current_user_id()
    requests_service.add(upload=False, download=True, get_columns=False, task_type='None', model_type='None',
                         cur_used_id=-1)
    downloaded_data = files_service.preprocessed_download()
    return StreamingResponse(downloaded_data, media_type='csv',
                             headers={'Content-Disposition': 'attachment; filename=fuel_consumption_prep.csv'})


@router.get('/get_columns', name='Получить названия столбцов')
def columns(files_service: FilesService = Depends(),
            requests_service: FilesRequestsService = Depends(),
            users_service: UserService = Depends(),
            ):
    # user_id = get_current_user_id()
    requests_service.add(upload=False, download=False, get_columns=True, task_type='None', model_type='None',
                         cur_used_id=-1)
    return files_service.df_columns()


@router.post('/regression_models',
             name='Обучение моделей под регрессию (ridge, decision tree, bagging)')
def regression_models(model_name: str, column_name: str, files_service: FilesService = Depends(),
                      requests_service: FilesRequestsService = Depends(),
                      users_service: UserService = Depends(),
                      ):
    # user_id = get_current_user_id()
    requests_service.add(upload=False, download=False, get_columns=False,
                         task_type='regression', model_type=model_name,
                         cur_used_id=-1)
    if model_name == 'ridge':
        return files_service.regression_ridge(column_name)
    elif model_name == 'decision tree':
        return files_service.regression_decisiontree(column_name)
    elif model_name == 'bagging':
        return files_service.regression_bag(column_name)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующая модель')


@router.post('/classification_models',
             name='Обучение моделей под классификацию (knn, logistic regression, decision tree)',
             response_class=PlainTextResponse)
async def classification_models(model_name: str, column_name: str, files_service: FilesService = Depends(),
                                requests_service: FilesRequestsService = Depends(),
                                users_service: UserService = Depends(),
                                ):
    # user_id = get_current_user_id()
    requests_service.add(upload=False, download=False, get_columns=False,
                         task_type='classification', model_type=model_name,
                         cur_used_id=-1)
    if model_name == 'knn':
        return files_service.classification_knn(column_name)
    if model_name == 'logistic regression':
        return files_service.classification_log_reg(column_name)
    if model_name == 'decision tree':
        return files_service.classification_dt(column_name)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Несуществующая модель')

