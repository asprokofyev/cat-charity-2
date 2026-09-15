from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest

router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
CurrentUser = Annotated[User, Depends(current_user)]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    summary='Get All Donations',
    description='Показать список всех пожертвований.',
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: SessionDep,
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    summary='Get My Donations',
    description='Показать список моих пожертвований.',
)
async def get_my_donations(user: CurrentUser, session: SessionDep):
    return await donation_crud.get_by_user(user.id, session)


@router.post(
    '/',
    response_model=DonationDB,
    summary='Create Donation',
    description='Создать пожертвование.',
)
async def create_donation(
    donation: DonationCreate,
    user: CurrentUser,
    session: SessionDep,
):
    donation_data = donation.model_dump()
    donation_data['user_id'] = user.id
    db_donation = await donation_crud.create(
        donation_data, session, commit=False
    )
    await invest(session, db_donation)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation
