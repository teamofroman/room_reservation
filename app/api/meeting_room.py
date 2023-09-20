from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.utils import check_unique_room_name, get_room_by_id
from app.crud.meeting_room import (
    crud_create_meeting_room,
    crud_delete_meeting_room,
    crud_read_all_meeting_rooms_db,
    crud_update_meeting_room,
)
from app.schemas.meeting_room import (
    SchemasMeetingRoomCreate,
    SchemasMeetingRoomDB,
    SchemasMeetingRoomUpdate,
)

router = APIRouter(prefix='/meeting_rooms', tags=['Meeting rooms'])


@router.post(
    '/',
    response_model=SchemasMeetingRoomDB,
    response_model_exclude_none=True,
    summary='Create meeting room',
)
async def api_create_new_meeting_room(
    meeting_room: SchemasMeetingRoomCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_unique_room_name(meeting_room.name, session)
    new_room = await crud_create_meeting_room(meeting_room, session)
    return new_room


@router.get(
    '/',
    response_model=list[SchemasMeetingRoomDB],
    response_model_exclude_none=True,
    summary='Get list of meeting room',
)
async def api_get_all_meeting_room(
    session: AsyncSession = Depends(get_async_session),
):
    rooms = await crud_read_all_meeting_rooms_db(session)
    return rooms


@router.patch(
    '/{meeting_room_id}/',
    response_model=SchemasMeetingRoomDB,
    response_model_exclude_none=True,
    summary='Update meeting room information',
)
async def api_partially_update_meeting_room(
    meeting_room_id: int,
    obj_in: SchemasMeetingRoomUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await get_room_by_id(meeting_room_id, session)

    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорная не существует',
        )

    if obj_in.name is not None:
        await check_unique_room_name(obj_in.name, session)

    meeting_room = await crud_update_meeting_room(
        meeting_room, obj_in, session
    )

    return meeting_room


@router.delete(
    '/{meeting_room_id}/',
    response_model=SchemasMeetingRoomDB,
    response_model_exclude_none=True,
    summary='Delete meeting room',
)
async def api_delete_meeting_room(
    meeting_room_id: int, session: AsyncSession = Depends(get_async_session)
):
    meeting_room = await get_room_by_id(meeting_room_id, session)

    if meeting_room is None:
        raise HTTPException(
            status_code=404,
            detail='Переговорная не существует',
        )

    meeting_room = await crud_delete_meeting_room(meeting_room, session)
    return meeting_room
