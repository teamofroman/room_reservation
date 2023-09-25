from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import ModelReservation


class CRUDReservation(CRUDBase):
    async def get_reservations_at_the_same_time(
        self,
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        reservation_id: Optional[int] = None,
        session: AsyncSession
    ) -> list[ModelReservation]:
        select_rtmt = select(ModelReservation).where(
            ModelReservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= ModelReservation.to_reserve,
                to_reserve >= ModelReservation.from_reserve,
            ),
        )

        if reservation_id:
            select_rtmt = select_rtmt.where(
                ModelReservation.id != reservation_id
            )
        reservations = await session.execute(select_rtmt)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
        self, meetingroom_id: int, session: AsyncSession
    ) -> list[ModelReservation]:
        reservations = await session.execute(
            select(ModelReservation).where(
                ModelReservation.meetingroom_id == meetingroom_id,
                ModelReservation.to_reserve > datetime.now(),
            )
        )

        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(ModelReservation)
