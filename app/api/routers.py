from fastapi import APIRouter

from app.api.endpoints import charity_project_router, donation_router
from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

main_router = APIRouter()

main_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Аутентификация'],
)
main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Аутентификация'],
)
main_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['Пользователи'],
)
main_router.include_router(
    charity_project_router,
    prefix='/charity_project',
    tags=['Целевые проекты'],
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Пожертвования'],
)
