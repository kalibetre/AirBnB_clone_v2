#!/usr/bin/python3
"""Module base_model

This Module contains a definition for User Class
"""

from sqlalchemy import Column, String

from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """A class that represents a user.

    Attributes:
        email (str): The email of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
