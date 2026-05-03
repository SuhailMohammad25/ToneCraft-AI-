from datetime import datetime, timezone
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_message: Mapped[str] = mapped_column(Text, nullable=False)
    brand_tone: Mapped[str] = mapped_column(String(40), nullable=False)
    channel: Mapped[str] = mapped_column(String(40), nullable=False)
    company_context: Mapped[str | None] = mapped_column(Text, nullable=True)
    agent_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str] = mapped_column(String(30), nullable=False)
    emotion: Mapped[str] = mapped_column(String(40), nullable=False)
    intensity: Mapped[int] = mapped_column(Integer, nullable=False)
    emotion_reason: Mapped[str] = mapped_column(Text, nullable=False)
    tone_adjustment: Mapped[str] = mapped_column(Text, nullable=False)
    main_reply: Mapped[str] = mapped_column(Text, nullable=False)
    short_reply: Mapped[str] = mapped_column(Text, nullable=False)
    detailed_reply: Mapped[str] = mapped_column(Text, nullable=False)
    de_escalation_reply: Mapped[str] = mapped_column(Text, nullable=False)
    guidance_do: Mapped[str] = mapped_column(Text, nullable=False)
    guidance_dont: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
