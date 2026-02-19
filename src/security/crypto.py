import os
import hashlib
from cryptography.fernet import Fernet, InvalidToken

def get_fernet() -> Fernet:
    key = os.getenv("FERNET_KEY")
    if not key:
        raise RuntimeError("FERNET_KEY mungon në .env")
    return Fernet(key.encode())

def encrypt_text(value: str) -> str:
    f = get_fernet()
    token = f.encrypt(value.encode("utf-8"))
    return token.decode("utf-8")

def decrypt_text(token: str) -> str:
    f = get_fernet()
    try:
        value = f.decrypt(token.encode("utf-8"))
        return value.decode("utf-8")
    except InvalidToken as e:
        raise ValueError("Token i pavlefshëm") from e

def hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()