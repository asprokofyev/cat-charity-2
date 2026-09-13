from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.core.config import settings


class Base(DeclarativeBase):
    pass


class CommonMixin:
    __abstract__ = True

    create_date: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    close_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    invested_amount: Mapped[int] = mapped_column(default=0, nullable=False)
    fully_invested: Mapped[bool] = mapped_column(default=False)


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
