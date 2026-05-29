from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    category: Mapped[str | None] = mapped_column(String(30))

    trends: Mapped[list["SkillTrend"]] = relationship(back_populates="skill")


class SkillTrend(Base):
    __tablename__ = "skill_trends"
    __table_args__ = (UniqueConstraint("skill_id", "snapshot_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False)
    count_7d: Mapped[int] = mapped_column(Integer, default=0)
    count_30d: Mapped[int] = mapped_column(Integer, default=0)
    delta_7d: Mapped[float] = mapped_column(Float, default=0.0)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)

    skill: Mapped["Skill"] = relationship(back_populates="trends")
