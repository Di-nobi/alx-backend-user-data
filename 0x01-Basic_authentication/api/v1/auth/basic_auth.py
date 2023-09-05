#!/usr/bin/env python3
"""Basic Authentication"""
from api.v1.auth.auth import Auth
from typing import List

class BasicAuth(Auth):
    """Basic Authentication that inherits from Auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extraction of base64 authorization"""
        if authorization_header is None and type(authorization_header) is not str:
            return None
        if  authorization_header.split(" ")[0] != 'Basic':
            return None
        return authorization_header.split(" ")[1]
        