from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from extensions import db


class ReceivedItem(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    recieved_at: Mapped[datetime] = mapped_column(default=func.now())
