from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime
from datetime import datetime

from database.db import Base

class Reservations(Base):
    __tablename__ = 'reservations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id", ondelete="CASCADE"))
    reservation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    table: Mapped["Tables"] = relationship("Tables", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation(id={self.id}, customer_name='{self.customer_name}', table_id={self.table_id}, time={self.reservation_time})>"