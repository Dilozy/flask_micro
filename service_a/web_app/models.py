from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from web_app.extensions import db


class Item(db.Model):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=func.now())


class OutboxEvent(db.Model):
    __tablename__ = "outbox_events"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=func.now())
    processed: Mapped[bool] = mapped_column(db.Boolean, default=False)
    payload: Mapped[dict] = mapped_column(db.JSON, nullable=False)
