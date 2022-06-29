from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts",tags=["posts"])

# 7:58
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # using raw sql
    # cursor.execute("SELECT * FROM post")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.Post, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING * ",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM post WHERE id = %s",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM post WHERE id = %s RETURNING *",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post.first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
def update_post(id: int, post: schemas.Post,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post = db.query(models.Post).filter(models.Post.id == id).first()
    updated_post.update(**post.dict(),synchronize_session=False)
    db.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return updated_post