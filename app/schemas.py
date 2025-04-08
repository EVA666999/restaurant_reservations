from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional

class Location(str, Enum):
    """Table locations"""
    MAIN_HALL = "Main Hall"
    TERRACE = "Terrace"
    GARDEN = "Garden"
    PRIVATE_ROOM = "Private Room"
    BAR_AREA = "Bar Area"

class CreateTable(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Name of the table")
    seats: int = Field(..., gt=0, le=100, description="Number of seats at the table")
    location: Location = Field(..., description="Location of the table in the restaurant")