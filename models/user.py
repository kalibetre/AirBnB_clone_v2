#!/usr/bin/python3
"""Module base_model

This Module contains a definition for User Class
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """A class that represents a user.

    Attributes:
        email : The email of the user.
        password : The password of the user.
        first_name : The first name of the user.
        last_name : The last name of the user.
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    places = relationship(
        "Place",
        cascade='all, delete, delete-orphan',
        backref="user",
    )
    reviews = relationship(
        "Review",
        cascade='all, delete, delete-orphan',
        backref="user",
    )
