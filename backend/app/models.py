from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Guest(Base):
    __tablename__ = "guests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Progress(Base):
    __tablename__ = "progress"

    guest_id: Mapped[str] = mapped_column(String(36), ForeignKey("guests.id"), primary_key=True)
    campaign_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    unlocked_quest_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    completed_quest_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    last_language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guest_id: Mapped[str] = mapped_column(String(36), index=True)
    quest_id: Mapped[str] = mapped_column(String(64), index=True)
    language: Mapped[str] = mapped_column(String(32))
    mode: Mapped[str] = mapped_column(String(16))
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
