# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
# pylint: disable=C0116
# pylint: disable=C0144
# pylint: disable=W0622.

from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["argon2"],deprecated="auto")
def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)