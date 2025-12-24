from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime

class ReportBase(BaseModel):
    prompt: str

class ReportCreate(ReportBase):
    pass

class ReportSchema(ReportBase):
    id: int
    user_id: int
    content: Any  # JSON structure
    created_at: datetime

    class Config:
        from_attributes = True

class PDFTaskSchema(BaseModel):
    id: int
    status: str
    file_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
