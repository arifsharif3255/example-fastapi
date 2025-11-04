# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
# pylint: disable=C0116
# pylint: disable=C0144
# pylint: disable=W0622.

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import session
from .. import database, schemas, models, utils, Oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router=APIRouter(tags=["AUTHENTICATION"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")
    
    access_token=Oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
 