from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Report(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    prompt = Column(Text, nullable=False)
    # Storing structured JSON response from Gemini
    content = Column(JSON, nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    owner = relationship("User", backref="reports")

class PDFTask(Base):
    __tablename__ = "pdf_tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    report_id = Column(Integer, ForeignKey("report.id"))
    status = Column(String, default="PENDING", index=True) # PENDING, PROCESSING, COMPLETED, FAILED
    file_path = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    report = relationship("Report")
