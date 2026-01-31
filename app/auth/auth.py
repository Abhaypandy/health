import os
import hashlib
import hmac
import base64

ITERATIONS = 260000  # OWASP recommended range

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATIONS
    )
    return base64.b64encode(salt + key).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    decoded = base64.b64decode(hashed_password.encode())
    salt = decoded[:16]
    stored_key = decoded[16:]

    new_key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATIONS
    )
    return hmac.compare_digest(stored_key, new_key)
