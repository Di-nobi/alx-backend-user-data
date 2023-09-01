#!/usr/bin/env python3
"""Encryption of data"""
import bcrypt

def hash_password(password: str) -> bytes:
    """Encodes password"""
    hash_password = bcrypt.hashpw( password.encode('utf-8'), bcrypt.gensalt())
    return hash_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)