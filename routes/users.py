from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException

from db.database import get_db
from db.models.users_model import User
from schemas.users import UserCreate, UserSchema
from serices.users_services import create_user, get_user_by_email

router = APIRouter()


@router.get("/users", response_model=List[UserSchema])
async def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/users", response_model=UserSchema, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_user(db=db, user=user)
