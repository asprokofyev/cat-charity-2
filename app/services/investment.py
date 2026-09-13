from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


async def invest(
    session: AsyncSession,
    target: CharityProject | Donation,
) -> None:
    if isinstance(target, CharityProject):
        donations_result = await session.execute(
            select(Donation).where(
                Donation.fully_invested == False  # noqa: E712
            ).order_by(Donation.create_date)
        )
        donations = donations_result.scalars().all()

        for donation in donations:
            if target.fully_invested:
                break

            free_amount = donation.full_amount - donation.invested_amount
            needed = target.full_amount - target.invested_amount
            invest_amount = min(free_amount, needed)

            donation.invested_amount += invest_amount
            target.invested_amount += invest_amount

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()  # type: ignore

            if target.invested_amount == target.full_amount:
                target.fully_invested = True
                target.close_date = datetime.now()  # type: ignore
    else:
        projects_result = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested == False  # noqa: E712
            ).order_by(CharityProject.create_date)
        )
        projects = projects_result.scalars().all()

        for project in projects:
            if target.fully_invested:
                break

            free_amount = target.full_amount - target.invested_amount
            needed = project.full_amount - project.invested_amount
            invest_amount = min(free_amount, needed)

            target.invested_amount += invest_amount
            project.invested_amount += invest_amount

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()  # type: ignore

            if target.invested_amount == target.full_amount:
                target.fully_invested = True
                target.close_date = datetime.now()  # type: ignore

    await session.commit()
