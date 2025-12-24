from fastapi import APIRouter
from app.api.v1 import auth, business, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(business.router, prefix="/business", tags=["business"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
