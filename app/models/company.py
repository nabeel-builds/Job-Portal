from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(100))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    owner: Mapped["User"] = relationship(back_populates="company")
    jobs: Mapped[list["Job"]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )