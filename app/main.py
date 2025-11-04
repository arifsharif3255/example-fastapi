
# ##  ///////////////////////////////code for understanding how fastapi works creates routs and paths with CRUD OPERATIONS////////////////////////////////////////

# # pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# from operator import index
# from random import randrange
# from fastapi import FastAPI, status, HTTPException, Response
# from fastapi.params import Body
# from pydantic import BaseModel



# app = FastAPI()




# my_posts = [{"title1 ": "this is title 1", "content": "here is the content", "id": 1},
#          {"title2":"here is title 2", "content":"here is content 2","id":2} ]


# class Post(BaseModel):
#     """Schema for a blog post including title, content, and publish status."""
#     title : str
#     content : str
#     published : bool=True




# def find_post(id: int):
#     for p in my_posts:
#         if p["id"]==id:
        
#             return p
        

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id']==id:
#             return i
        


# @app.get("/")
# def root():
#     return{"message":"hello world"}


# @app.get("/posts")
# def get_post():
#     return{"post_details": my_posts}



# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def get_posts(post: Post): # pylint: disable=missing-function-docstring
#     post_dict=post.dict()
#     post_dict['id']=randrange(0,100000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}

# @app.get("/posts/latest")
# def get_latest_post():
#     post=my_posts[len(my_posts)-1]
#     return{"details": post}

# @app.get("/posts/{id}")
# def get_single_post(id: int):
#     post= find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post having {id} not found")
#     return {"post_details": post}

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index=find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id:int, post:Post):
#     index=find_index_post(id)
#     if index==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} does not found")
    
#     post_dict=post.dict()
#     post_dict['id']= id
#     my_posts[index]=post_dict
#     return { "data": post_dict}
    









# ##  ///////////////////////////////code from AI with some changes and updates from AI ////////////////////////////////////////

# # pylint: disable=missing-module-docstring
# from datetime import datetime
# from fastapi import FastAPI, status, HTTPException, Response
# from pydantic import BaseModel

# app = FastAPI()

# # Initial posts
# my_posts = [
#     {"title": "this is title 1", "content": "here is the content", "id": 1, "created_at": "2025-10-23T10:00:00"},
#     {"title": "here is title 2", "content": "here is content 2", "id": 2, "created_at": "2025-10-23T10:05:00"}
# ]

# # Initialize the next_id to the highest ID + 1
# next_id = max(post["id"] for post in my_posts) + 1 if my_posts else 1


# class Post(BaseModel):
#     """Schema for a blog post including title, content, and publish status."""
#     title: str
#     content: str
#     published: bool = True


# def find_post(post_id: int):
#     for p in my_posts:
#         if p["id"] == post_id:
#             return p


# def find_index_post(post_id: int):
#     for i, p in enumerate(my_posts):
#         if p["id"] == post_id:
#             return i
#     return None


# @app.get("/")
# def root():
#     return {"message": "hello world"}


# @app.get("/posts")
# def get_posts():
#     return {"post_details": my_posts}


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     global next_id
#     post_dict = post.model_dump()
#     post_dict["id"] = next_id
#     post_dict["created_at"] = datetime.utcnow().isoformat()  # UTC timestamp
#     next_id += 1
#     my_posts.append(post_dict)
#     return {"data": post_dict}


# @app.get("/posts/latest")
# def get_latest_post():
#     if not my_posts:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="No posts available")
#     post = my_posts[-1]
#     return {"details": post}


# @app.get("/posts/{id}")
# def get_single_post(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} not found")
#     return {"post_details": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} does not exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     index = find_index_post(id)
#     if index is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} not found")

#     post_dict = post.model_dump()
#     post_dict["id"] = id
#     post_dict["created_at"] = my_posts[index]["created_at"]  # keep original timestamp
#     my_posts[index] = post_dict
#     return {"data": post_dict}










# ##  ///////////////////////////////manipulation codes for playing with database////////////////////////////////////////

# # pylint: disable=missing-module-docstring
# from operator import index
# from random import randrange
# import time
# from fastapi import FastAPI, status, HTTPException, Response
# from fastapi.params import Body
# from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor


# app = FastAPI()


# class Post(BaseModel):
#     """Schema for a blog post including title, content, and publish status."""
#     title : str
#     content : str
#     published : bool=True


# my_posts = [{"title1 ": "this is title 1", "content": "here is the content", "id": 1},
#          {"title2":"here is title 2", "content":"here is content 2","id":2} ]


# while True:
#     try:
#         Conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='khan0551391', cursor_factory=RealDictCursor)
#         cursor=Conn.cursor()
#         print("database connected")
#         break
#     except Exception as error:
#         print("connection with DB failed")
#         print("error:", error)
#         time.sleep(2)

# def find_post(post_id: int):
#     for p in my_posts:
#         if p["id"] == post_id:
#             return p

# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     posts=cursor.fetchall()
#     return{"data": posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute(""" insert into posts (title, content, published) values (%s, %s, %s)
#                     returning*""",
#                     (post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     Conn.commit()
#     return{"data": new_post}

# @app.get("/posts/latest")
# def get_latest_post():
#     cursor.execute("""select * from posts order by id desc limit 1;""")
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="No posts available")
#     return {"data": post}

# @app.get("/posts/{id}")
# def get_single_post(id: int):
#     cursor.execute("""select * from posts where id=%s""",(str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} not found")
#     return {"data": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#        cursor.execute("""delete from posts where id=%s returning *""",(str(id),))
#        deleted_post = cursor.fetchone()
#        Conn.commit()
#        if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
#        return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute("""update posts set title=%s, content=%s, published=%s where id=%s returning *""", (post.title, post.content, post.published, str(id),))
#     updated_post=cursor.fetchone()
#     Conn.commit()
#     if updated_post== None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with id {id} not found")
#     return{"data": updated_post}







# ###  ///////////////////////////////Practicing of ORM object relational mapping i-e manipulation of DB without using SQL Queries like used in above practice////////////////////////////////////////
# ###  ///////////////////////////////using SQLAlchemy ORM////////////////////////////////////////

# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
from fastapi import FastAPI
from sqlalchemy import engine
from .database import engine
from . import models
from app.routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

