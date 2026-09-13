from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, CommonMixin


class CharityProject(CommonMixin, Base):
    __tablename__ = "charityproject"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
