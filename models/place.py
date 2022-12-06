#!/usr/bin/python3
"""Module base_model

This Module contains a definition for Place Class
"""

from os import getenv

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

import models
from models.base_model import Base, BaseModel
from models.review import Review


class Place(BaseModel, Base):
    """A class that represents a place

    Attributes:
        city_id (str): The City id.
        user_id (str): The User id.
        name (str): The name of the place.
        description (str): The description of the place.
        number_rooms (int): The number of rooms of the place.
        number_bathrooms (int): The number of bathrooms of the place.
        max_guest (int): The maximum number of guests of the place.
        price_by_night (int): The price by night of the place.
        latitude (float): The latitude of the place.
        longitude (float): The longitude of the place.
        amenity_ids (list): A list of Amenity ids.
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

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Get list of reviews that match this place id"""
            return [
                v for _, v in models.storage.all(Review).items()
                if v.place_id == self.id
            ]
    else:
        reviews = relationship(
            "Review",
            cascade="all, delete, delete-orphan",
            backref=backref("place"),)
