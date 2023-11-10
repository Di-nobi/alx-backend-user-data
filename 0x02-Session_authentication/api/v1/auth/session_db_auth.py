#!/usr/bin/env python3
"""Database """

from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Database class Authentication"""

    def create_session(self, user_id=None):
        """Creates and stores new instance of UserSession 
        and returns the Session ID"""
        session_data = super().create_session(user_id)
        if not session_data:
            return None
        myList = {
            "user_id": user_id,
            "session_id": session_data
        }
        usr_session = UserSession(**myList)
        usr_session.save()
        return session_data
    
    def user_id_for_session_id(self, session_id=None):
        """"Gets the user id"""
        usr = UserSession.search({'session_id': session_id})
        if not usr:
            return None
        current = datetime.now()
        if self.session_duration <= 0:
            return usr[0].user_id
        expire_time = usr[0].created_at + timedelta(seconds=self.session_duration)
        if expire_time <= current:
            return None
        return usr[0].user_id
    
    def destroy_session(self, request=None):
        """Destroys the current session"""
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False
        if sessions:
            UserSession.remove(sessions[0])
            return True
        return False
    