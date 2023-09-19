from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.db import AsyncSessionLocal
from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import MeetingRoomCreate


async def get_room_id_by_name(
    room_name: str, session: AsyncSession
) -> Optional[int]:
    # async with AsyncSessionLocal() as session:
    db_room_id = await session.execute(
        select(MeetingRoom.id).where(
            MeetingRoom.name == room_name,
        )
    )
    db_room_id = db_room_id.scalars().first()
    return db_room_id


async def create_meeting_room(
    new_room: MeetingRoomCreate, session: AsyncSession
) -> MeetingRoom:
    new_room_data = new_room.dict()
    db_room = MeetingRoom(**new_room_data)
    # Убираем контекстный менеджер, т.к. передаем сессию из вне
    # async with AsyncSessionLocal() as session:
    session.add(db_room)
    # Записываем изменения непосредственно в БД.
    # Так как сессия асинхронная, используем ключевое слово await.
    await session.commit()
    # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    await session.refresh(db_room)

    return db_room


async def read_all_rooms_db(session: AsyncSession):
    db_rooms = await session.execute(select(MeetingRoom))
    db_rooms = db_rooms.scalars().all()
    return db_rooms
