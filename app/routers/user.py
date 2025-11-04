# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
# pylint: disable=C0116
# pylint: disable=W0622
# pylint: disable=W0613
# pylint: disable=W0301
# pylint: disable=W0311
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import session
from ..database import session, get_db
from .. import models, schemas, utils


router=APIRouter(tags=['users'])



@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db:session=Depends(get_db)):
    hashed_password=utils.hash(user.password)

    user.password=hashed_password

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_single_user(id: int, db:session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")
    return user


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db:session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id) # pylint: disable=W0311
    if user.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)