from functools import wraps

from flask import current_app, request, jsonify, g
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from models import Admin

TOKEN_MAX_AGE_SECONDS = 8 * 60 * 60  # 8 hours


def _serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="admin-auth")


def generate_admin_token(admin_id):
    return _serializer().dumps({"admin_id": admin_id})


def admin_required(view_func):
    """Require a valid 'Authorization: Bearer <token>' header for admin-only routes."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ", 1)[1].strip()
        try:
            data = _serializer().loads(token, max_age=TOKEN_MAX_AGE_SECONDS)
        except SignatureExpired:
            return jsonify({"error": "Session expired, please log in again"}), 401
        except BadSignature:
            return jsonify({"error": "Invalid session token"}), 401

        admin = Admin.query.get(data.get("admin_id"))
        if not admin:
            return jsonify({"error": "Admin account no longer exists"}), 401

        g.admin = admin
        return view_func(*args, **kwargs)

    return wrapper
