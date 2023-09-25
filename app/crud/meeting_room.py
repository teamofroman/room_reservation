from sqlalchemy.ext.asyncio import AsyncSession

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
    db_room = await meeting_room_crud.create(new_room, session)

    return db_room


async def crud_read_all_meeting_rooms_db(session: AsyncSession):
    db_rooms = await meeting_room_crud.get_multi(session)
    return db_rooms


async def crud_update_meeting_room(
    db_room: ModelMeetingRoom,
    room_in: SchemasMeetingRoomUpdate,
    session: AsyncSession,
):
    db_room = await meeting_room_crud.update(db_room, room_in, session)

    return db_room


async def crud_delete_meeting_room(
    room: ModelMeetingRoom,
    session: AsyncSession,
):
    room = await meeting_room_crud.remove(room, session)
    return room
