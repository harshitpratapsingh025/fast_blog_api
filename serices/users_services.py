from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.users_model import User, UserProfile
from schemas.users import UserCreate, CreateUserProfile, UpdateUserProfile
from passlib.context import CryptContext


def get_password_hash(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_profile(db: Session, profile: CreateUserProfile, user: User):
    db_profile = UserProfile(
        education=profile.education,
        addess=profile.addess,
        city=profile.city,
        state=profile.state,
        pincode=profile.pincode,
        language_id=profile.language_id,
        country_id=profile.country_id,
        user_id=user.id,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_user_profile(db: Session, profile: UpdateUserProfile):
    try:
        user_profile = (
            db.query(UserProfile).filter(UserProfile.id == profile.id).first()
        )
        if not user_profile:
            raise HTTPException(status_code=400, detail="Invalid profile ID.")
        user_profile.education = profile.education
        user_profile.addess = profile.addess
        user_profile.city = profile.city
        user_profile.state = profile.state
        user_profile.image = profile.image
        user_profile.pincode = profile.pincode
        user_profile.language_id = profile.language_id
        user_profile.country_id = profile.country_id
        db.commit()
        return user_profile

    except Exception as error:
        raise HTTPException(status_code=400, detail=f"error is {error}")
