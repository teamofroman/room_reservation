from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.meeting_room import ModelMeetingRoom


async def check_unique_room_name(room_name: str, session: AsyncSession):
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорная с таким именем уже существует',
        )


async def get_room_id_by_name(
    room_name: str, session: AsyncSession
) -> Optional[int]:
    # async with AsyncSessionLocal() as session:
    db_room_id = await session.execute(
        select(ModelMeetingRoom.id).where(
            ModelMeetingRoom.name == room_name,
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def get_room_by_id(
    room_id: int, session: AsyncSession
) -> Optional[ModelMeetingRoom]:
    db_room = await session.execute(
        select(ModelMeetingRoom).where(
            ModelMeetingRoom.id == room_id,
        )
    )
    db_room = db_room.scalar()
    return db_room
