#!/usr/bin/python3
"""Module base_model

This Module contains a definition for City Class
"""

from sqlalchemy import Column, ForeignKey, String

from models.base_model import Base, BaseModel


class City(BaseModel, Base):
    """A class that represents a city

    Attributes:
        name (str): name of the city
        state_id (str): the state id
    """
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
