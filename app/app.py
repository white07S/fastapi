from multiprocessing import synchronize
from requests import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body

from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host = 'localhost',database='fastapi', user='postgres', password='root',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected')
        break
    except Exception as e:
        print('Database not connected')
        print(e)
        time.sleep(5)


    
    
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}






