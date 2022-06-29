from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users",tags=['Users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user( user: schemas.UserCreate,db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user