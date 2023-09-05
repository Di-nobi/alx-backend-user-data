#!/usr/bin/env python3
"""Authentication process"""
from flask import request
from typing import List, TypeVar

class Auth():
    """Authentication class setter"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """An authentication Public method"""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        for i in excluded_paths:
            if i[0] == path:
                return False
            if i[-1] == "*" or i[-1] == '/':
                if i[:-1] == path:
                    return False
        return True
    def authorization_header(self, request=None) -> str:
        """Header Authorization"""
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Current User"""
        return None

    