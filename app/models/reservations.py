from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy import DateTime
from datetime import datetime

from app.database.db import Base

class Reservations(Base):
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id", ondelete="CASCADE"))
    reservation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)