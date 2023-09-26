from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_room_exists, check_room_name_duplicate
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud
from app.schemas.meeting_room import (
    SchemasMeetingRoomCreate,
    SchemasMeetingRoomDB,
    SchemasMeetingRoomUpdate,
)
from app.schemas.reservation import SchemaReservationDB

router = APIRouter()


@router.post(
    '/',
    response_model=SchemasMeetingRoomDB,
    response_model_exclude_none=True,
    summary='Create meeting room',
    dependencies=[Depends(current_superuser)],
)
async def api_create_new_meeting_room(
        meeting_room: SchemasMeetingRoomCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для администраторов."""
    await check_room_name_duplicate(meeting_room.name, session)
    new_room = await meeting_room_crud.create(meeting_room, session)
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
    rooms = await meeting_room_crud.get_multi(session)
    return rooms


@router.patch(
    '/{meeting_room_id}/',
    response_model=SchemasMeetingRoomDB,
    response_model_exclude_none=True,
    summary='Update meeting room information',
    dependencies=[Depends(current_superuser)],
)
async def api_partially_update_meeting_room(
        meeting_room_id: int,
        obj_in: SchemasMeetingRoomUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    meeting_room = await check_room_exists(meeting_room_id, session)

    if obj_in.name is not None:
        await check_room_name_duplicate(obj_in.name, session)

    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )

    return meeting_room


@router.delete(
    '/{meeting_room_id}/',
    response_model=SchemasMeetingRoomDB,
    response_model_exclude_none=True,
    summary='Delete meeting room',
    dependencies=[Depends(current_superuser)],
)
async def api_delete_meeting_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    meeting_room = await check_room_exists(meeting_room_id, session)

    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room


@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[SchemaReservationDB],
    summary='Get room reservation times',
    response_model_exclude={'user_id'},
)
async def api_get_reservations_for_room(
        meeting_room_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await check_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        meetingroom_id=meeting_room_id, session=session
    )
    return reservations
