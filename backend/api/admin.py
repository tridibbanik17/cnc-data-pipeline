from flask import Blueprint, jsonify, request
from db.connection import get_connection
from services.jwt_guard import require_auth, require_role

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/users", methods=["GET"])
@require_auth
@require_role(["admin"])
def list_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, username, role
        FROM users
        ORDER BY id ASC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = []
    for r in rows:
        users.append({
            "id": r[0],
            "username": r[1],
            "role": r[2]
        })

    return jsonify(users)


@admin_bp.route("/admin/users/<int:user_id>/role", methods=["PUT"])
@require_auth
@require_role(["admin"])
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get("role")

    if new_role not in ["operator", "admin"]:
        return jsonify({"error": "invalid role"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET role = %s
        WHERE id = %s
    """, (new_role, user_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "updated"})