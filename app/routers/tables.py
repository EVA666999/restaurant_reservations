from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import delete, insert, select, update
from slugify import slugify
from schemas import CreateTable
from models.tables import TableLocation, Tables
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_depends import get_db

router = APIRouter(prefix='/tables', tags=['tables'])


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_tables(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.scalars(select(Tables))
    tables = result.all()
    if not tables:
         raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no table found'
            )
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
        name=create_table.name,
        seats=create_table.seats,
        location=TableLocation(create_table.location.value)
    )

    db.add(new_table)
    await db.commit()
    await db.refresh(new_table)

    return {"detail": "Table created successfully", "id": new_table.id}

@router.delete('/{table_id}', status_code=status.HTTP_200_OK)
async def delete_table(db: Annotated[AsyncSession, Depends(get_db)], table_id: int):
        table = await db.scalar(select(Tables).where(Tables.id == table_id))
        if table is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no table found'
            )
        await db.delete(table)
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Table delete is successful'
        }
