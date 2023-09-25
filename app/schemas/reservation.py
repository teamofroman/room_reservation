from datetime import datetime

from pydantic import BaseModel, Extra, root_validator, validator


class SchemaReservationBase(BaseModel):
    from_reserve: datetime
    to_reserve: datetime

    class Config:
        extra = Extra.forbid


class SchemaReservationDB(SchemaReservationBase):
    id: int
    meetingroom_id: int

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
