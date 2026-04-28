import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

SECRET = "super_secret_key_change_me"

def hash_password(password: str):
    return generate_password_hash(password)

def verify_password(password: str, hashed: str):
    return check_password_hash(hashed, password)

def create_token(user_id: int, username: str, role: str):
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, SECRET, algorithms=["HS256"])