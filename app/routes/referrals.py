from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import Referral, ReferralCreate, ReferralUpdate, ReferralModel, Status
from app.database import get_db

router = APIRouter(prefix="/api/referrals", tags=["Referrals"])


@router.get("", response_model=List[Referral])
def list_referrals(
    status:      Optional[Status] = None,
    assigned_to: Optional[str]   = None,
    db: Session = Depends(get_db),
):
    """כל הפניות — סינון אופציונלי לפי סטטוס / נציג."""
    query = db.query(ReferralModel)
    if status:
        query = query.filter(ReferralModel.status == status)
    if assigned_to:
        query = query.filter(ReferralModel.assigned_to == assigned_to)
    return query.all()


@router.get("/mine/{agent_name}", response_model=List[Referral])
def get_my_referrals(
    agent_name:  str,
    status:      Optional[Status] = None,
    db: Session = Depends(get_db),
):
    """הפניות שלי — לפי שם נציג."""
    query = db.query(ReferralModel).filter(ReferralModel.assigned_to == agent_name)
    if status:
        query = query.filter(ReferralModel.status == status)
    results = query.all()
    if not results:
        raise HTTPException(404, f"No referrals found for '{agent_name}'")
    return results


@router.get("/{referral_id}", response_model=Referral)
def get_referral(referral_id: int, db: Session = Depends(get_db)):
    """פנייה בודדת לפי ID."""
    ref = db.query(ReferralModel).filter(ReferralModel.id == referral_id).first()
    if not ref:
        raise HTTPException(404, f"Referral {referral_id} not found")
    return ref


@router.post("", response_model=Referral, status_code=201)
def create_referral(body: ReferralCreate, db: Session = Depends(get_db)):
    """יצירת פנייה חדשה."""
    ref = ReferralModel(**body.model_dump())
    db.add(ref)
    db.commit()
    db.refresh(ref)
    return ref


@router.patch("/{referral_id}", response_model=Referral)
def update_referral(referral_id: int, body: ReferralUpdate, db: Session = Depends(get_db)):
    """עדכון שדות פנייה (חלקי)."""
    ref = db.query(ReferralModel).filter(ReferralModel.id == referral_id).first()
    if not ref:
        raise HTTPException(404, f"Referral {referral_id} not found")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(ref, field, value)
    db.commit()
    db.refresh(ref)
    return ref


@router.patch("/{referral_id}/status", response_model=Referral)
def update_status(referral_id: int, status: Status, db: Session = Depends(get_db)):
    """עדכון סטטוס בלבד."""
    ref = db.query(ReferralModel).filter(ReferralModel.id == referral_id).first()
    if not ref:
        raise HTTPException(404, f"Referral {referral_id} not found")
    ref.status = status
    db.commit()
    db.refresh(ref)
    return ref


@router.delete("/{referral_id}", status_code=204)
def delete_referral(referral_id: int, db: Session = Depends(get_db)):
    """מחיקת פנייה."""
    ref = db.query(ReferralModel).filter(ReferralModel.id == referral_id).first()
    if not ref:
        raise HTTPException(404, f"Referral {referral_id} not found")
    db.delete(ref)
    db.commit()