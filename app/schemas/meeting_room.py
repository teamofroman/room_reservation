from typing import Optional

from pydantic import BaseModel, Field, validator


class SchemasMeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class SchemasMeetingRoomCreate(SchemasMeetingRoomBase):
    name: str = Field(..., min_length=2, max_length=100)

    class Config:
        title = 'Комната для переговоров'


class SchemasMeetingRoomDB(SchemasMeetingRoomBase):
    id: int

    class Config:
        orm_mode = True


class SchemasMeetingRoomUpdate(SchemasMeetingRoomBase):
    @validator('name')
    def name_cannot_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым')

        return value
