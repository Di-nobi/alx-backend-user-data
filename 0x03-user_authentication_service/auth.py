#!/usr/bin/env python3
"""Encrypt My Users Passwords from Frauds and Freaks
Authentication file that dialogues with the API for 
the validation of a user
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

def _hash_password(password: str) -> bytes:
    """Hashes the password and returns it in bytes
    Args: passwords: password in string foermat
    """
    encrypt = password.encode('utf-8')
    return bcrypt.hashpw(encrypt, bcrypt.gensalt())

def _generate_uuid() -> str:
    """Generates a uuid, returning a string format"""
    UUID = str(uuid4())
    return UUID

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email: str, password: str):
        """Registers a user to the database"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
    
    def valid_login(self, email: str, password: str) -> bool:
        """Validates a password"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
    def create_session(self, email: str):
        """Gets a session id"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id
    
    def get_user_from_session_id(self, session_id: str):
        """Gets a user from a session id"""
        try:
            session_user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return session_user
    def destroy_session(self, user_id):
        """Destroys a session"""
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None
        return None
    def get_reset_password_token(self, email: str):
        """Generates a reset password token for a user
        Args:
            email: str
        """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError
        UUID = _generate_uuid()
        self._db.update_user(user.id, reset_token=UUID)
        return UUID
