#!/usr/bin/python3
"""Module base_model

This Module contains a definition for State Class
"""

from os import getenv

from sqlalchemy import Column, String
from sqlalchemy.orm import backref, relationship

import models
from models.base_model import Base, BaseModel
from models.city import City


class State(BaseModel, Base):
    """A class that represents a state

    Attribute:
        name : the name of the state
    """
    __table_args__ = ({'mysql_default_charset': 'latin1'})
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":

        @property
        def cities(self):
            """Get list of cities that match this state id"""
            return [
                v for _, v in models.storage.all(City).items()
                if v.state_id == self.id
            ]
    else:
        cities = relationship(
            "City",
            cascade="all, delete, delete-orphan",
            backref=backref("state"),
        )
