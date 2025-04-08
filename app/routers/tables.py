from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import delete, insert, select, update
from slugify import slugify
from fastapi_limiter.depends import RateLimiter
from schemas import CreateTable
from models.tables import Tables
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db

router = APIRouter(prefix='/tables', tags=['tables'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_tables(db: Annotated[AsyncSession, Depends(get_db)]):
    tables = db.scalars(select(Tables)).all()
    return tables

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создание стола"
)
async def create_table(
    db: Annotated[AsyncSession, Depends(get_db)],
    create_table: CreateTable):
    """Создает новый стол"""
    new_table = Tables(
        name = create_table.name,
        seats = create_table.seats,
        location = create_table.location
    )

    db.add(new_table)
    await db.commit()
    await db.refresh(new_table)

    response = {"detail": "Table created successfully", "id": new_table.id}


    return response