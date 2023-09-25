from fastapi import APIRouter

from app.api.endpoints import (
    meetingroom_router,
    reservation_router,
    user_router,
)

main_router = APIRouter()

main_router.include_router(
    meetingroom_router, prefix='/meeting_rooms', tags=['Meeting rooms']
)

main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservation rooms']
)

main_router.include_router(user_router)
