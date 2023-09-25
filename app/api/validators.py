from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.meeting_room import meeting_room_crud
from app.crud.reservation import reservation_crud


async def check_room_name_duplicate(room_name: str, session: AsyncSession):
    room = await meeting_room_crud.get_by_attribute('name', room_name, session)
    if room is not None:
        raise HTTPException(
            status_code=422, detail='Комната с таким именем уже существует!'
        )


async def check_room_exists(room_id, session: AsyncSession):
    room = await meeting_room_crud.get(room_id, session)
    if room is None:
        raise HTTPException(status_code=422, detail='Комната не найдена!')

    return room


async def check_reservation_intersections(**kwargs) -> None:
    reservations = await reservation_crud.get_reservations_at_the_same_time(
        **kwargs)
    if reservations:
        raise HTTPException(
            status_code=422,
            detail=str(reservations)
        )