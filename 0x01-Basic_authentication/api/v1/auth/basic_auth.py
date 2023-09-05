#!/usr/bin/env python3
"""Basic Authentication"""
from .auth import Auth
from typing import List
import base64
from models.user import User
from typing import TypeVar

class BasicAuth(Auth):
    """Basic Authentication that inherits from Auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extraction of base64 authorization"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[-1]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Password"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode = base64_authorization_header.encode('utf-8')
            decode = base64.b64decode(decode)
            return decode.decode('utf-8')
        except Exception:
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """A method that returns a username and password"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return decoded_base64_authorization_header.split(":")[0], ":".join(decoded_base64_authorization_header.split(":")[1:])
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns User Object"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        usr = User.search({"email": user_email})
        if not usr:
            return None
        for user in usr:
            if user.is_valid_password(user_pwd):
                return user
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """A basicauth that overloads Auth and retrives the User instance"""
        authhead = self.authorization_header(request)
        if not authhead:
            return None
        base = self.extract_base64_authorization_header(authhead)
        if not base:
            return None
        decode = self.decode_base64_authorization_header(base)
        if not decode:
            return None
        arg1, arg2 = self.extract_user_credentials(decode)
        if arg1 is None or arg2 is None:
            return None
        usr = self.user_object_from_credentials(arg1, arg2)
        return usr