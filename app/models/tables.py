from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Enum
import enum
from typing import List, TYPE_CHECKING
from database.db import Base

if TYPE_CHECKING:
    from .reservations import Reservations

class TableLocation(enum.Enum):
    """Table locations"""
    MAIN_HALL = "Главный зал"
    TERRACE = "Терраса"
    GARDEN = "Сад"
    PRIVATE_ROOM = "Приватная комната"
    BAR_AREA = "Барная зона"

class Tables(Base):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[TableLocation] = mapped_column(Enum(TableLocation), nullable=False)
    
    reservations: Mapped[List["Reservations"]] = relationship("Reservations", 
        back_populates="table", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Table(id={self.id}, name='{self.name}', seats={self.seats}, location={self.location.value})>"