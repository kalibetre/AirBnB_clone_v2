#!/usr/bin/python3
"""Module base_model

This Module contains a definition for BaseModel Class
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

import models

Base = declarative_base()


class BaseModel:
    """BaseModel Class"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """__init__ method & instantiation of class BaseModel

        Args:
            *args.
            **kwargs (dict): Key/value pairs
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs is not None and len(kwargs) > 0:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                elif k in ["created_at", "updated_at"]:
                    setattr(self, k, datetime.fromisoformat(v))
                else:
                    setattr(self, k, v)

    def save(self):
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)

    def to_dict(self):
        """
        returns a dictionary containing all
        keys/values of __dict__ of the instance
        """
        bs_dict = ({
            k: (v.isoformat() if isinstance(v, datetime) else v)
            for (k, v) in self.__dict__.items()
        })
        bs_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in list(bs_dict.keys()):
            del bs_dict["_sa_instance_state"]
        return bs_dict

    def __str__(self) -> str:
        """should print/str representation of the BaseModel instance."""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.to_dict(),
        )
