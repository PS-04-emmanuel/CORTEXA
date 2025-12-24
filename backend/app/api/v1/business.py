from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.schemas.business import ReportSchema, ReportCreate
from app.models.user import User
from app.services.gemini_service import gemini_service
from app.services.pdf_service import pdf_service
from app.db.repositories.report_repo import report_repo
from app.models.business import Report

router = APIRouter()

@router.post("/generate-report", response_model=ReportSchema)
async def generate_report(
    *,
    db: AsyncSession = Depends(deps.get_db),
    report_in: ReportCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # 1. Call Gemini
    ai_response = await gemini_service.generate_report(report_in.prompt)
    
    if "error" in ai_response:
        raise HTTPException(status_code=500, detail=ai_response["error"])

    # 2. Save to DB
    report = Report(
        user_id=current_user.id,
        prompt=report_in.prompt,
        content=ai_response
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report

@router.get("/reports", response_model=List[ReportSchema])
async def read_reports(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 6,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    reports = await report_repo.get_multi_by_user(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return reports

@router.post("/reports/{report_id}/pdf")
async def create_pdf_task(
    report_id: int,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    report = await report_repo.get(db, id=report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Synchronous PDF generation for immediate download
    try:
        pdf_bytes = pdf_service.generate_report_pdf(report.content)
        return StreamingResponse(
            io.BytesIO(pdf_bytes), 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=report_{report_id}.pdf"}
        )
    except Exception as e:
        print(f"PDF Gen Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")
