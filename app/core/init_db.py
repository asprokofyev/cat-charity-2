from fastapi_users.exceptions import UserAlreadyExists

from app.core.db import AsyncSessionLocal
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


async def create_user(
    email: str, password: str, is_superuser: bool = False
):
    try:
        async with AsyncSessionLocal() as session:
            async for user_db in get_user_db(session):
                async for user_manager in get_user_manager(user_db):
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )
    except UserAlreadyExists:
        pass
