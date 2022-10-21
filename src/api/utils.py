import hashlib
import base64
from core.config import app_config
import secrets


def pbkdf2(password: str, iterations: int = 100_000, dklen: int = 0, digest=hashlib.sha256):
    dklen = dklen or None
    password = password.encode("utf-8")
    salt = app_config.HASH_SALT.encode("utf-8")
    return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)


def hash_password(password: str, iterations: int = 100_000, salt: str = app_config.HASH_SALT) -> str:
    hash = pbkdf2(password)
    hash = base64.b64encode(hash).decode('ascii').strip()
    return "sha-256$%d$%s$%s" % (iterations, salt, hash)


def constant_time_compare(val1: str, val2: str):
    """Return True if the two strings are equal, False otherwise."""
    return secrets.compare_digest(val1.encode("utf-8"), val2.encode("utf-8"))


def check_password(password: str, hashed_password: str) -> bool:
    return constant_time_compare(hash_password(password), hashed_password)
