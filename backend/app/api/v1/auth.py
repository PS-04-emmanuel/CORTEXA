from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.user import UserCreate, User, UserLogin
from app.db.repositories.user_repo import user_repo
from app.core.config import settings
from app.core import security

router = APIRouter()

@router.post("/signup", response_model=User)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    user = await user_repo.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_repo.create_user(db, obj_in=user_in)
    return user

@router.post("/login")
async def login_access_token(
    user_in: UserLogin,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    user = await user_repo.get_by_email(db, email=user_in.email)
    
    if not user or not security.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
        "is_onboarded": user.is_onboarded
    }
