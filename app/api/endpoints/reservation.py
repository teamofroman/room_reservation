from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_room_exists, \
    check_reservation_intersections, check_reservation_before_edit
from app.core.db import get_async_session
from app.crud.reservation import reservation_crud
from app.schemas.reservation import SchemaReservationDB, \
    SchemaReservationCreate

router = APIRouter()


@router.post(
    '/',
    response_model=SchemaReservationDB,
    summary='Reservation room'
)
async def api_create_new_reservation(
        reservation: SchemaReservationCreate,
        session: AsyncSession = Depends(get_async_session),
):
    room = await check_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(
        **reservation.dict(), session=session,
    )
    new_reservation = await reservation_crud.create(reservation, session)
    return new_reservation


@router.get(
    '/',
    response_model=list[SchemaReservationDB],
    summary='List of reserved room',
)
async def api_get_all_reserved_room(
        session: AsyncSession = Depends(get_async_session)
):
    reserved_rooms = await reservation_crud.get_multi(session)
    return reserved_rooms


@router.delete(
    '/{reservation_id:int}',
    response_model=SchemaReservationDB,
    summary='Remove room reservation',
)
async def api_delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(reservation_id, session)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation
