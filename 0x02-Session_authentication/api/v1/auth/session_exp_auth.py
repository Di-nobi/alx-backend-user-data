#!/usr/bin/env python3
"""Session Expiration"""
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os
#import datetime
from datetime import datetime, timedelta
class SessionExpAuth(SessionAuth):
    """Session Expiration Class Instance"""
    def __init__(self):
        self.session_duration = int(os.getenv('SESSION_DURATION'))
        if not self.session_duration or type(self.session_duration) != int:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creating of a SESSION ID"""
        session = super().create_session(user_id)
        if not session:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session] = session_dictionary
        return session
    
    def user_id_for_session_id(self, session_id=None):
        """Gets a User for its session id"""
        if not session_id:
            return None
        details = self.user_id_by_session_id.get(session_id)
        if not details:
            return None
        if not details.get("created_at"):
            return None
        if self.session_duration <= 0:
            return details.get("user_id")
        if details.get("created_at") + timedelta(seconds=self.session_duration) <= datetime.now():
            return None
        return details.get("user_id")