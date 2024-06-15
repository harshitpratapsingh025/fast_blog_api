from fastapi import APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from db.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from serices.auth import authenticate_user, create_access_token
from schemas.auth import Token


router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
