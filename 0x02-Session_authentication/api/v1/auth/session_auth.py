#!/usr/bin/env python3
"""A Session Authentication"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid

class SessionAuth(Auth):
    """A session class that inherits from Auth"""
    user_id_by_session_id = dict()
    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        UUID = str(uuid.uuid4())
        self.user_id_by_session_id[UUID] = user_id
        return UUID
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """A session that returns user based on id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
    def current_user(self, request=None):
        """Session ID used for identifying a User"""
        cookie = self.session_cookie(request)
        session = self.user_id_for_session_id(cookie)
        usr = User.get(session)
        return usr
    def destroy_session(self, request=None):
        """Deletes the user session/logout"""
        if request is None:
            return False
        session = self.session_cookie(request)
        if not session:
            return False
        if not self.user_id_for_session_id(session):
            return False
        del self.user_id_by_session_id[session]
        return True