#!/usr/bin/python3
"""Module base_model

This Module contains a definition for Place Class
"""

from os import getenv

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import backref, relationship

import models
from models.base_model import Base, BaseModel
from models.review import Review

place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False,
    ),
    Column(
        'amenity_id',
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False,
    ),
)


class Place(BaseModel, Base):
    """A class that represents a place

    Attributes:
        city_id : The City id.
        user_id : The User id.
        name : The name of the place.
        description : The description of the place.
        number_rooms : The number of rooms of the place.
        number_bathrooms : The number of bathrooms of the place.
        max_guest : The maximum number of guests of the place.
        price_by_night : The price by night of the place.
        latitude : The latitude of the place.
        longitude : The longitude of the place.
        amenity_ids : A list of Amenity ids.
    """

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)

    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def reviews(self):
            """Get list of reviews that match this place id"""
            return [
                v for _, v in models.storage.all(Review).items()
                if v.place_id == self.id
            ]

        @property
        def amenities(self):
            """returns list of amenity ids"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, value=None):
            """appends aminity id"""
            type_name = type(value).__name__
            if type_name == 'Amenity' and value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
    else:
        reviews = relationship("Review",
                               cascade="all, delete, delete-orphan",
                               backref=backref("place"))
        amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            viewonly=False,
            back_populates="place_amenities",
        )
