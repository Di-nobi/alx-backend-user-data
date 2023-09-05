#!/usr/bin/env python3
"""Basic Authentication"""
from .auth import Auth
from typing import List
import base64

class BasicAuth(Auth):
    """Basic Authentication that inherits from Auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extraction of base64 authorization"""
        if authorization_header is None or type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[-1]
        