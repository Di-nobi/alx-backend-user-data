#!/usr/bin/env python3
"""Database Module"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a user to the database
        Args:
            email: Users email address
            hashed_password: password hashed
        Return Created User
        """
        usr = User(email=email, hashed_password=hashed_password)
        self._session.add(usr)
        self._session.commit()
        return usr
    
    def find_user_by(self, **kwargs):
        """
        Finds a user in the database
        Kwargs: key and value argument of a user detail
        Return: User found
        """
        session = self._session
        find = session.query(User).filter_by(**kwargs).first()
        if not find:
            raise NoResultFound
        return find
    
    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user"""
        DATA = ["id", "session_id", "email", "hashed_password", "reset_token"]
        save = self._session.commit()
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in DATA:
                raise ValueError
            setattr(user, key, value)
        save
        return None

