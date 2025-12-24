from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.repository import BaseRepository
from app.models.business import Report

class ReportRepository(BaseRepository[Report]):
    async def get_multi_by_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 6
    ) -> List[Report]:
        result = await db.execute(
            select(Report)
            .filter(Report.user_id == user_id)
            .order_by(desc(Report.created_at))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

report_repo = ReportRepository(Report)
