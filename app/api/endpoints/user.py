# app/api/endpoints/user.py
from fastapi import APIRouter, HTTPException

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import (
    SchemasUserCreate,
    SchemasUserRead,
    SchemasUserUpdate,
)

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(SchemasUserRead, SchemasUserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(SchemasUserRead, SchemasUserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True,
)
def api_delete_user(id: str):
    raise HTTPException(
        status_code=405, detail='Удаление пользователей запрещено!'
    )
