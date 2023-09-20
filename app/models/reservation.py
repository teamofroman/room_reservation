from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class ModelReservation(Base):
    from_reserve = Column(DateTime)
    to_reserve = Column(DateTime)
    meetingroom_id = Column(Integer, ForeignKey('modelmeetingroom.id'))
