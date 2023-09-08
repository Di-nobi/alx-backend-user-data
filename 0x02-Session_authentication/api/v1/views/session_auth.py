#!/usr/bin/env python3
"""New view for Session Authentication"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth():
    """Retrieves user name and password"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or email == []:
        return jsonify({"error": "email missing"}), 400
    if not password or password == []:
        return jsonify({"error": "password missing"}), 400
    
    usr = User.search({"email": email})
    if not usr:
        return jsonify({"error": "no user found for this email"}), 401
    for user in usr:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        session = auth.create_session(user.id)
        res = jsonify(user.to_json())
        data = os.getenv('SESSION_NAME')
        res.set_cookie(data, session)
        return res
        
@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def delete_session():
    """Deletes the session auth"""
    from api.v1.app import auth
    delete_session = auth.destroy_session(request)
    if not delete_session:
        abort(404)
    return jsonify({}), 200 