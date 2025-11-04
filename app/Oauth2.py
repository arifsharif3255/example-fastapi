# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
# pylint: disable=C0116
# pylint: disable=C0144
# pylint: disable=W0622.

from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRETE_KEY="0ADAD3A32503D03AF30F3AF"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data: dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt=jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload=jwt.decode(token,SECRETE_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str= Depends(oauth2_scheme), db:session= Depends(database.get_db)):
    credential_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not velidate credentials", headers={"WWW-Authenticate":"Bearer"})
    toke_datan= verify_access_token(token, credential_exception)
    user=db.query(models.User).filter(models.User.id==toke_datan.id).first()
    return user