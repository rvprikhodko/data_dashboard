from fastapi import APIRouter
from src.api import users
from src.api import files

router = APIRouter()

router.include_router(users.router)
router.include_router(files.router)

