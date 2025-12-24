from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.user import UserUpdate
from app.db.repositories.user_repo import user_repo

router = APIRouter()

@router.put("/me/onboard", response_model=Any)
async def complete_onboarding(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # Update user status
    current_user.is_onboarded = True
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return {"msg": "Onboarding completed", "is_onboarded": True}
