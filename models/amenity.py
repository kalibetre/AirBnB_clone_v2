#!/usr/bin/python3
"""Module base_model

This Module contains a definition for Amenity Class
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """A class that represents a amenity

    Attribute:
        name (str): the name of the amenity
    """

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
