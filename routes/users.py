from fastapi import APIRouter
from sqlalchemy.orm import Session
from typing import List
from fastapi import Depends, HTTPException

from db.database import get_db
from db.models.users_model import User
from schemas.users import (
    UserCreate,
    UserSchema,
    CreateUserProfile,
    UserProfileSchema,
    UpdateUserProfile,
)
from serices import users_services
from serices.auth import get_current_active_user

router = APIRouter()


@router.post("/users", response_model=UserSchema, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users_services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return users_services.create_user(db=db, user=user)


@router.get("/users", response_model=List[UserSchema])
async def read_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    return db.query(User).all()


@router.post("/user/profile", response_model=UserProfileSchema, status_code=201)
async def create_user_profile(
    profile: CreateUserProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return users_services.create_user_profile(db=db, profile=profile, user=current_user)


@router.put("/user/profile", response_model=UserProfileSchema, status_code=201)
async def update_user_profile(
    profile: UpdateUserProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return users_services.update_user_profile(db=db, profile=profile, user=current_user)
