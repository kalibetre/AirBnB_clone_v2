#!/usr/bin/python3
"""Module base_model

This Module contains a definition for City Class
"""

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class City(BaseModel, Base):
    """A class that represents a city

    Attributes:
        name : name of the city
        state_id : the state id
    """
    __table_args__ = ({'mysql_default_charset': 'latin1'})
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
    places = relationship(
        "Place",
        cascade='all, delete, delete-orphan',
        backref="cities",
    )
