from sqlalchemy import Boolean, Integer, Column, String
from sqlalchemy.orm import relationship
from database import Base


class Entry(Base):
    __tablename__ = 'entry'

    uuid = Column(String, primary_key=True, unique=True)
    text = Column(String)
