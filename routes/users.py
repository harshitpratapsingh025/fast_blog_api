from fastapi import APIRouter, File, UploadFile
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
user_router = APIRouter(prefix="/user")


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


@user_router.post("/profile", response_model=UserProfileSchema, status_code=201)
async def create_user_profile(
    profile: CreateUserProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return users_services.create_user_profile(db=db, profile=profile, user=current_user)


@user_router.put("/profile", response_model=UserProfileSchema, status_code=201)
async def update_user_profile(
    profile: UpdateUserProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return users_services.update_user_profile(db=db, profile=profile, user=current_user)


@user_router.post("/upload")
def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return users_services.update_user_profile_image(db=db, file=file, user=current_user)


@user_router.post("/add_interests", response_model=bool, status_code=201)
async def add_user_interests(
    categories: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return users_services.add_user_interests(
        db=db, category_list=categories, user=current_user
    )
