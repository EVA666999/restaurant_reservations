from datetime import timedelta, timezone
from typing import Annotated

from database.db_depends import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from models.reservations import Reservations
from models.tables import Tables
from schemas import CreateReservation
from slugify import slugify
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reservations", tags=["reservations"])


MSK_TIME = timezone(timedelta(hours=3))


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_reservations(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.scalars(select(Reservations))
    reservations = result.all()
    if not reservations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no reservations found",
        )
    return reservations


@router.post("/", status_code=status.HTTP_201_CREATED, summary="Создание брони")
async def create_reservations(
    db: Annotated[AsyncSession, Depends(get_db)], create_reservation: CreateReservation
):
    """Забронировать стол"""

    table_query = select(Tables).where(Tables.id == create_reservation.table_id)
    table_time = await db.execute(table_query)
    table = table_time.scalar_one_or_none()

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Стол с ID {create_reservation.table_id} не найден",
        )

    reservation_time = create_reservation.reservation_time.astimezone(MSK_TIME).replace(
        tzinfo=None
    )
    new_reservation_end_time = reservation_time + timedelta(
        minutes=create_reservation.duration_minutes
    )

    existing_reservations_query = (
        select(Reservations)
        .where(Reservations.table_id == create_reservation.table_id)
        .order_by(Reservations.reservation_time)
    )

    existing_reservations_result = await db.execute(existing_reservations_query)
    existing_reservations = existing_reservations_result.scalars().all()

    next_available_time = None
    for existing_reservation in existing_reservations:
        existing_end_time = existing_reservation.reservation_time + timedelta(
            minutes=existing_reservation.duration_minutes
        )

        if (
            reservation_time < existing_end_time
            and new_reservation_end_time > existing_reservation.reservation_time
        ):
            if next_available_time is None or existing_end_time < next_available_time:
                next_available_time = existing_end_time

    if next_available_time is not None:
        error_detail = "Стол уже забронирован на это время"
        formatted_time = next_available_time.strftime("%H:%M %d.%m.%Y")
        error_detail += f". Стол будет доступен после: {formatted_time}"

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error_detail
        )

    new_reservation = Reservations(
        customer_name=create_reservation.customer_name,
        table_id=create_reservation.table_id,
        reservation_time=reservation_time,
        duration_minutes=create_reservation.duration_minutes,
    )

    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)

    return {"detail": "Reservation created successfully", "id": new_reservation.id}


@router.delete("/{reservation_id}", status_code=status.HTTP_200_OK)
async def delete_table(
    db: Annotated[AsyncSession, Depends(get_db)], reservation_id: int
):
    reservation = await db.scalar(
        select(Reservations).where(Reservations.id == reservation_id)
    )
    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no reservation found",
        )
    await db.delete(reservation)
    await db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Reservation delete is successful",
    }
