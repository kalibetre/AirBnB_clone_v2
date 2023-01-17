#!/usr/bin/python3
"""Module base_model

This Module contains a definition for Amenity Class
"""

from sqlalchemy import Column, ForeignKey, String

from models.base_model import Base, BaseModel


class Review(BaseModel, Base):
    """A class that represents a review

    Attributes:
        place_id : The Place id.
        user_id : The User id.
        text : The text of the review.
    """
    __table_args__ = ({'mysql_default_charset': 'latin1'})
    __tablename__ = "reviews"
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    text = Column(String(1024), nullable=False)
