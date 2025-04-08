from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Enum
import enum

from app.database.db import Base

class TableLocation(enum.Enum):
    """table locations"""
    MAIN_HALL = "Main Hall"
    TERRACE = "Terrace"
    GARDEN = "Garden"
    PRIVATE_ROOM = "Private Room"
    BAR_AREA = "Bar Area"

class Tables(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[TableLocation] = mapped_column(Enum(TableLocation), nullable=False)

    def __repr__(self):
        return f"<Table(id={self.id}, name='{self.name}', seats={self.seats}, location={self.location.value})>"
    
