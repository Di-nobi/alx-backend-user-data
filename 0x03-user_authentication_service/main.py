#!/usr/bin/env python3
""" Main File """
import request


def register_user(email: str, password: str) -> None:
    """Registers a User"""
    payload = {"email": email, "password": password}
    data = request.post("http://192.168.43.205:5000/users", payload)
    assert data.status_code == 200
    assert data.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """ Checks for wrong password"""
    payload = {"email": email, "password": password}
    data = request.post("http://192.168.43.205:5000/sessions", payload)
    assert data.status_code == 200
    assert data.json() == {"email": email, "message": "Invalid Credientials"}


def log_in(email: str, password: str) -> str:
    """ Checks for wrong password"""
    payload = {"email": email, "password": password}
    data = request.post("http://192.168.43.205:5000/sessions", payload)
    assert data.status_code == 200
    assert data.json() == {"email": email, "message": "logged in"}
    return data.cookies.get('session_id')


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
