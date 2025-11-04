
# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
# pylint: disable=C0116
# pylint: disable=W0622
# pylint: disable=W0613
# pylint: disable=W0301
from typing import Optional, List
from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import session
from ..database import session, get_db
from .. import models, Oauth2, schemas, database


router = APIRouter(tags=['posts'])


# @router.get("/posts", response_model=list[schemas.Post])
# def get_posts(db: session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     posts = db.query(models.Post).filter(
#         models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     return posts

@router.get("/posts", response_model=List[schemas.PostOut])
def get_posts(
    db: session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    posts = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/latest", response_model=schemas.Post)
def get_latest_post(db: session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).order_by(
        models.Post.created_at.desc()).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )
    return post


@router.get("/posts/{id}", response_model=schemas.Post)
def get_single_post(id: int, db: session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorize to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
