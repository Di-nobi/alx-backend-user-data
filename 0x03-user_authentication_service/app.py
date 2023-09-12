#!/usr/bin/env  python3
"""Flask App"""
from flask import jsonify
from flask import Flask
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
    """Logs in a user"""
    email = request.form.get('email')
    password = request.form.get('password')
    login_usr = AUTH.valid_login(email, password)
    if not login_usr:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "Logged in"})
    response.set_cookie("session_id", session_id)
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
