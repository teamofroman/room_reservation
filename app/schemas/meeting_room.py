from typing import Optional

from pydantic import BaseModel, Field, validator


class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class MeetingRoomCreate(MeetingRoomBase):
    name: str = Field(..., min_length=2, max_length=100)

    class Config:
        title = 'Комната для переговоров'


class MeetingRoomDB(MeetingRoomBase):
    id: int

    class Config:
        orm_mode = True


class MeetingRoomUpdate(MeetingRoomBase):
    @validator('name')
    def name_cannot_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым')

        return value
