from datetime import datetime

from sqlalchemy import and_, between, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.reservation import ModelReservation


class CRUDReservation(CRUDBase):
    async def get_reservations_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            meetingroom_id: int,
            session: AsyncSession
    ) -> list[ModelReservation]:
        reservations = await session.execute(
            select(ModelReservation).where(
                ModelReservation.meetingroom_id == meetingroom_id,
                and_(
                    from_reserve <= ModelReservation.to_reserve,
                    to_reserve >= ModelReservation.from_reserve
                )
            )
        )
        reservations = reservations.scalars().all()
        return reservations


reservation_crud = CRUDReservation(ModelReservation)
