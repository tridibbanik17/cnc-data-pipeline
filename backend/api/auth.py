from flask import Blueprint, request, jsonify
from db.connection import get_connection
from services.auth_service import hash_password, verify_password, create_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "operator")   # NEW

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    # Validate role
    if role not in ["operator", "admin"]:
        return jsonify({"error": "invalid role"}), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users(username, password_hash, role)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (username, hash_password(password), role))

        user_id = cur.fetchone()[0]
        conn.commit()

    except Exception:
        conn.rollback()
        return jsonify({"error": "username already exists"}), 409

    finally:
        cur.close()
        conn.close()

    return jsonify({"status": "created", "user_id": user_id, "role": role})


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, password_hash, role
        FROM users
        WHERE username = %s
    """, (username,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "invalid credentials"}), 401

    user_id, password_hash_db, role = row

    if not verify_password(password, password_hash_db):
        return jsonify({"error": "invalid credentials"}), 401

    token = create_token(user_id, username, role)

    return jsonify({"token": token, "role": role})