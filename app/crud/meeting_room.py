from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from app.core.db import AsyncSessionLocal
from app.crud.base import CRUDBase
from app.models.meeting_room import ModelMeetingRoom
from app.schemas.meeting_room import (
    SchemasMeetingRoomCreate,
    SchemasMeetingRoomUpdate,
)

meeting_room_crud = CRUDBase(ModelMeetingRoom)


async def crud_create_meeting_room(
        new_room: SchemasMeetingRoomCreate, session: AsyncSession
) -> ModelMeetingRoom:
    new_room_data = new_room.dict()
    db_room = ModelMeetingRoom(**new_room_data)
    # Убираем контекстный менеджер, т.к. передаем сессию из вне
    # async with AsyncSessionLocal() as session:
    session.add(db_room)
    # Записываем изменения непосредственно в БД.
    # Так как сессия асинхронная, используем ключевое слово await.
    await session.commit()
    # Обновляем объект db_room: считываем данные из БД, чтобы получить его id.
    await session.refresh(db_room)

    return db_room


async def crud_read_all_meeting_rooms_db(session: AsyncSession):
    db_rooms = await session.execute(select(ModelMeetingRoom))
    db_rooms = db_rooms.scalars().all()
    return db_rooms


async def crud_update_meeting_room(
        db_room: ModelMeetingRoom,
        room_in: SchemasMeetingRoomUpdate,
        session: AsyncSession,
):
    # Переводим объект с данными из БД в словарь
    obj_data = jsonable_encoder(db_room)

    # Переводим объект из запроса в словарь
    update_data = room_in.dict(exclude_unset=True)

    for field in obj_data:
        if field in update_data:
            setattr(db_room, field, update_data[field])

    session.add(db_room)
    await session.commit()
    await session.refresh(db_room)

    return db_room


async def crud_delete_meeting_room(
        room: ModelMeetingRoom,
        session: AsyncSession,
):
    await session.delete(room)
    await session.commit()
    return room
