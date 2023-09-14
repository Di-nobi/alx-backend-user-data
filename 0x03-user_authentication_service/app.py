#!/usr/bin/env  python3
"""Flask App"""
from flask import jsonify
from flask import Flask, redirect
from flask import abort
from user import User
from auth import Auth
from flask import request

AUTH = Auth()

app = Flask(__name__)

@app.route("/", methods=['GET'], strict_slashes=False)
def index() -> str:
    """Basic flask message"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def reg_users():
    """Registers a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        reg_usr = AUTH.register_user(email, password)
        return jsonify({"email": reg_usr.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Logs in a user if the credientials are valid"""
    email = request.form.get('email')
    password = request.form.get('password')
    login_usr = AUTH.valid_login(email, password)
    if not login_usr:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "Logged in"})
    response.set_cookie("session_id", session_id)
    return response
@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logouts out a user by deleting current session"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile():
    """Gets the profile of a user"""
    session = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)
@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_token():
    """
    Gets a reset password token for a user
    """
    email = request.form.get("email")
    user = AUTH.get_reset_password_token(email)
    if not user:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{user}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
