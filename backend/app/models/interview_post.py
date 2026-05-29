from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, SmallInteger, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InterviewPost(Base):
    __tablename__ = "interview_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int | None] = mapped_column(ForeignKey("companies.id"))
    company_name: Mapped[str | None] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    rounds: Mapped[int | None] = mapped_column(SmallInteger)
    difficulty: Mapped[int | None] = mapped_column(SmallInteger)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    questions: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    author_name: Mapped[str] = mapped_column(String(50), default="匿名")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    likes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
