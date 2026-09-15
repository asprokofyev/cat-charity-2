from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_invested_amount_before_update,
    check_name_duplicate,
    check_project_can_be_deleted,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Get All Charity Projects',
    description='Показать список всех целевых проектов.',
)
async def get_all_charity_projects(
    session: SessionDep,
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Create Charity Project',
    description='Создать целевой проект.',
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: SessionDep,
):
    await check_name_duplicate(charity_project.name, session)

    db_project = await charity_project_crud.create(
        charity_project.model_dump(), session, commit=False
    )
    await invest(session, db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Update Charity Project',
    description='Редактировать целевой проект.',
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: SessionDep,
):
    db_project = await check_charity_project_exists(project_id, session)

    update_data = charity_project.model_dump(exclude_unset=True)

    await check_invested_amount_before_update(
        update_data, db_project, session
    )

    return await charity_project_crud.update(db_project, update_data, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Delete Charity Project',
    description='Удалить целевой проект.',
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: SessionDep,
):
    db_project = await check_charity_project_exists(project_id, session)
    check_project_can_be_deleted(db_project)

    return await charity_project_crud.remove(db_project, session)
