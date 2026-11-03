from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), index=True)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    salary_min: Mapped[Optional[int]]
    salary_max: Mapped[Optional[int]]
    is_active: Mapped[bool] = mapped_column(default=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="jobs")