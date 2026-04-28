from functools import wraps
from flask import request, jsonify
from services.auth_service import decode_token

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization")

        if not header or not header.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401

        token = header.split(" ")[1]

        try:
            user = decode_token(token)
            request.user = user
        except Exception:
            return jsonify({"error": "invalid or expired token"}), 401

        return f(*args, **kwargs)

    return wrapper


def require_role(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user or user.get("role") not in allowed_roles:
                return jsonify({"error": "forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator