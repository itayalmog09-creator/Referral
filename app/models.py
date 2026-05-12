from sqlalchemy import Column, Integer, String, Date, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from app.database import Base
 
 
# ─────────────────────────────────────────
# Enum
# ─────────────────────────────────────────
 
class Status(str, Enum):
    new         = "new"
    in_progress = "in_progress"
    waiting     = "waiting"
    closed      = "closed"
 
 
# ─────────────────────────────────────────
# טבלת מסד הנתונים
# ─────────────────────────────────────────
 
class ReferralModel(Base):
    """הטבלה שנוצרת אוטומטית במסד הנתונים."""
    __tablename__ = "referrals"
 
    id                 = Column(Integer, primary_key=True, index=True)
    name               = Column(String,  nullable=False)
    status             = Column(SAEnum(Status), nullable=False, default=Status.new)
    assigned_to        = Column(String,  nullable=True)
    next_followup_date = Column(Date,    nullable=True)
 
 
# ─────────────────────────────────────────
# Pydantic Schemas (קלט / פלט של ה-API)
# ─────────────────────────────────────────
 
class ReferralCreate(BaseModel):
    name:               str
    status:             Status             = Status.new
    assigned_to:        Optional[str]      = None
    next_followup_date: Optional[date]     = None
 
 
class ReferralUpdate(BaseModel):
    name:               Optional[str]      = None
    status:             Optional[Status]   = None
    assigned_to:        Optional[str]      = None
    next_followup_date: Optional[date]     = None
 
 
class AssignRequest(BaseModel):
    assigned_to: str
 
 
class Referral(BaseModel):
    id:                 int
    name:               str
    status:             Status
    assigned_to:        Optional[str]
    next_followup_date: Optional[date]
 
    class Config:
        from_attributes = True
 