from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, Extra, Field, root_validator, validator

FROM_TIME = (datetime.now() + timedelta(minutes=10)).isoformat(
    timespec='minutes'
)

TO_TIME = (datetime.now() + timedelta(hours=1)).isoformat(timespec='minutes')


class SchemaReservationBase(BaseModel):
    from_reserve: datetime = Field(..., example=FROM_TIME)
    to_reserve: datetime = Field(..., example=TO_TIME)

    class Config:
        extra = Extra.forbid


class SchemaReservationDB(SchemaReservationBase):
    id: int
    meetingroom_id: int
    user_id: Optional[int]

    class Config:
        orm_mode = True


class SchemaReservationUpdate(SchemaReservationBase):
    @validator('from_reserve')
    def check_from_reserve_later_than_now(cls, value: datetime):
        if value <= datetime.now():
            raise ValueError(
                'Время начала не может быть раньше текущего ' 'времени'
            )
        return value

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        if values['to_reserve'] <= values['from_reserve']:
            raise ValueError(
                'Время окончания должно быть больше времени ' 'начала'
            )
        return values


class SchemaReservationCreate(SchemaReservationUpdate):
    meetingroom_id: int
