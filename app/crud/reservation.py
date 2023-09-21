from app.crud.base import CRUDBase
from app.models.reservation import ModelReservation

reservation_crud = CRUDBase(ModelReservation)
