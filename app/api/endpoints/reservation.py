from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_reservation_before_edit,
    check_reservation_intersections,
    check_room_exists,
)
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.reservation import reservation_crud
from app.models import ModelUser
from app.schemas.reservation import (
    SchemaReservationCreate,
    SchemaReservationDB,
    SchemaReservationUpdate,
)

router = APIRouter()


@router.post(
    '/', response_model=SchemaReservationDB, summary='Reservation room'
)
async def api_create_new_reservation(
        reservation: SchemaReservationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: ModelUser = Depends(current_user),
):
    await check_room_exists(reservation.meetingroom_id, session)
    await check_reservation_intersections(
        **reservation.dict(),
        session=session,
    )
    new_reservation = await reservation_crud.create(reservation, session, user)
    return new_reservation


@router.get(
    '/',
    response_model=list[SchemaReservationDB],
    summary='List of reserved room',
    dependencies=[Depends(current_superuser)]
)
async def api_get_all_reserved_room(
        session: AsyncSession = Depends(get_async_session),
):
    reserved_rooms = await reservation_crud.get_multi(session)
    return reserved_rooms


@router.delete(
    '/{reservation_id:int}',
    response_model=SchemaReservationDB,
    summary='Remove room reservation',
)
async def api_delete_reservation(
        reservation_id: int, session: AsyncSession = Depends(get_async_session)
):
    reservation = await check_reservation_before_edit(reservation_id, session)
    reservation = await reservation_crud.remove(reservation, session)
    return reservation


@router.patch(
    '/{reservation_id:int}',
    response_model=SchemaReservationDB,
    summary='Update room reservation',
)
async def api_update_reservation(
        reservation_id: int,
        obj_in: SchemaReservationUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    reservation = await check_reservation_before_edit(reservation_id, session)
    await check_reservation_intersections(
        **obj_in.dict(),
        reservation_id=reservation_id,
        meetingroom_id=reservation.meetingroom_id,
        session=session,
    )
    reservation = await reservation_crud.update(
        db_obj=reservation, obj_in=obj_in, session=session
    )
    return reservation


@router.get(
    '/my_reservations',
    response_model=list[SchemaReservationDB],
    summary='Get my reservations',
    response_model_exclude={'user_id'},
)
async def api_get_my_reservations(
        user: ModelUser = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    reservations = await reservation_crud.get_by_user(
        user=user, session=session
    )
    return reservations
