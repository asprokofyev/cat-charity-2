from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self, name: str, session: AsyncSession
    ) -> int | None:
        result = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name)
        )
        return result.scalars().first()

    async def update(
        self, db_obj: CharityProject, obj_in, session: AsyncSession
    ) -> CharityProject:
        db_obj = await super().update(db_obj, obj_in, session)
        if (
            not db_obj.fully_invested and
            db_obj.invested_amount == db_obj.full_amount
        ):
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()  # type: ignore
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)
