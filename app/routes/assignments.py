from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Referral, AssignRequest, ReferralModel
from app.database import get_db
 
router = APIRouter(prefix="/api/referrals", tags=["Assignment"])
 
 
@router.post("/{referral_id}/assign", response_model=Referral)
def assign_referral(referral_id: int, body: AssignRequest, db: Session = Depends(get_db)):
    """הקצאת פנייה לנציג."""
    ref = db.query(ReferralModel).filter(ReferralModel.id == referral_id).first()
    if not ref:
        raise HTTPException(404, f"Referral {referral_id} not found")
    ref.assigned_to = body.assigned_to
    db.commit()
    db.refresh(ref)
    return ref