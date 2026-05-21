from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class Status(str, Enum):
    new         = "new"
    in_progress = "in_progress"
    waiting     = "waiting"
    closed      = "closed"


class ReferralCreate(BaseModel):
    name:               str
    status:             Status         = Status.new
    assigned_to:        Optional[str]  = None
    next_followup_date: Optional[date] = None


class ReferralUpdate(BaseModel):
    name:               Optional[str]    = None
    status:             Optional[Status] = None
    assigned_to:        Optional[str]    = None
    next_followup_date: Optional[date]   = None


class AssignRequest(BaseModel):
    assigned_to: str


class Referral(BaseModel):
    id:                 int
    name:               str
    status:             Status
    assigned_to:        Optional[str]
    next_followup_date: Optional[date]