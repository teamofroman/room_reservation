from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.meeting_room import (
    create_meeting_room,
    get_room_id_by_name,
    read_all_rooms_db, get_room_by_id, update_meeting_room, delete_room,
)
from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomDB, \
    MeetingRoomUpdate

router = APIRouter(prefix='/meeting_rooms', tags=['Meeting rooms'])


async def check_unique_room_name(room_name: str, session: AsyncSession):
    room_id = await get_room_id_by_name(room_name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Переговорная с таким именем уже существует',
        )


@router.post(
    '/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_unique_room_name(meeting_room.name, session)
    new_room = await create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_room(
        session: AsyncSession = Depends(get_async_session),
):
    rooms = await read_all_rooms_db(session)
    return rooms


@router.patch(
    '/{meeting_room_id}/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: MeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    meeting_room = await get_room_by_id(meeting_room_id, session)

    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорная не существует',
        )

    if obj_in.name is not None:
        await check_unique_room_name(obj_in.name, session)

    meeting_room = await update_meeting_room(
        meeting_room, obj_in, session,
    )

    return meeting_room


@router.delete(
    '/{meeting_room_id}/',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
)
async def delete_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    meeting_room = await get_room_by_id(meeting_room_id, session)

    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорная не существует',
        )

    meeting_room = await delete_room(meeting_room, session)
    return meeting_room
