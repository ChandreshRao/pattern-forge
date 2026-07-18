from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Progress(Base):
    """Durable progress for logged-in users only."""

    __tablename__ = "user_progress"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    campaign_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    unlocked_quest_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    completed_quest_ids_json: Mapped[str] = mapped_column(Text, default="[]")
    last_language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    guest_id: Mapped[str | None] = mapped_column(String(36), index=True, nullable=True)
    quest_id: Mapped[str] = mapped_column(String(64), index=True)
    language: Mapped[str] = mapped_column(String(32))
    mode: Mapped[str] = mapped_column(String(16))
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
