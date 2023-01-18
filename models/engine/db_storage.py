#!/usr/bin/python3
"""Module db_storage

This Module contains a definition for DBStorage Class
"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """FileStorage Class
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes DBStorage Class
        using the environment variables
        """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(user, pwd, host, db),
            pool_pre_ping=True,
        )

        if getenv("HBNB_ENV", "") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns the dictionary all or filtered objects"""
        all_objs = []
        _all_cls = [cls] if cls is not None else [
            State, City, User, Place, Review, Amenity
        ]
        for _cls in _all_cls:
            all_objs += self.__session.query(_cls)
        return {"{}.{}".format(type(v).__name__, v.id): v for v in all_objs}

    def new(self, obj):
        """adds the object to the current database session"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """commits all pending operations"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes a row from the database"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """reloads the memory values form database"""
        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine,
                                     expire_on_commit=False)
        Session = scoped_session(session_maker)
        self.__session = Session()

    def close(self):
        """cleanup method"""
        self.__session.close()
