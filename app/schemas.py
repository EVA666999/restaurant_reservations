from datetime import datetime, time, timedelta, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

RESTAURANT_CLOSE_HOUR = 22
RESTAURANT_CLOSE_MINUTE = 00

CLOSE_TIME = time(RESTAURANT_CLOSE_HOUR, RESTAURANT_CLOSE_MINUTE)

MAX_DURATION_MINUTES = 600


class Location(str, Enum):
    """Расположения столов в ресторане"""

    MAIN_HALL = "Главный зал"
    TERRACE = "Терраса"
    GARDEN = "Сад"
    PRIVATE_ROOM = "Приватная комната"
    BAR_AREA = "Барная зона"


class CreateTable(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Название стола")
    seats: int = Field(..., gt=0, le=100, description="Количество мест за столом")
    location: Location = Field(..., description="Расположение стола в ресторане")


class CreateReservation(BaseModel):
    customer_name: str = Field(
        ..., min_length=1, max_length=50, description="Имя клиента"
    )
    table_id: int = Field(..., gt=0, description="Id стола")
    reservation_time: datetime = Field(
        default=None, description="Время бронирования (МСК)"
    )
    duration_minutes: int = Field(
        ...,
        gt=15,
        le=MAX_DURATION_MINUTES,
        description="Длительность бронирования в минутах",
    )

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration(cls, duration, info):
        reservation_time = info.data.get("reservation_time", datetime.now(timezone.utc))

        if (reservation_time + timedelta(minutes=duration)).time() > CLOSE_TIME:
            raise ValueError(f"Бронирование не может заканчиваться после {CLOSE_TIME}")

        return duration
