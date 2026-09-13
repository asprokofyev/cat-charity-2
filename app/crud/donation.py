from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self, user_id: int, session: AsyncSession
    ) -> list[Donation]:
        result = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return list(result.scalars().all())


donation_crud = CRUDDonation(Donation)
