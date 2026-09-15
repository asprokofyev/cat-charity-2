from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str, session: AsyncSession, exclude_id: int | None = None
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session, exclude_id=exclude_id
    )
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


def check_project_is_closed(charity_project: CharityProject) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_full_amount_not_less_invested(
    new_full_amount: int,
    charity_project: CharityProject,
) -> None:
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail=(
                'Нельзя установить значение full_amount '
                'меньше уже вложенной суммы.'
            )
        )


def check_project_can_be_deleted(charity_project: CharityProject) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_invested_amount_before_update(
    update_data: dict,
    charity_project: CharityProject,
    session: AsyncSession,
) -> None:
    check_project_is_closed(charity_project)

    if "full_amount" in update_data:
        check_full_amount_not_less_invested(
            update_data["full_amount"], charity_project
        )

    if "name" in update_data:
        await check_name_duplicate(
            update_data["name"], session, exclude_id=charity_project.id
        )
