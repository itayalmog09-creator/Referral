from fastapi import APIRouter, HTTPException
from app.models import Referral, AssignRequest
from app import mock_db
 
router = APIRouter(prefix="/api/referrals", tags=["Assignment"])
 
 
@router.post("/{referral_id}/assign", response_model=Referral)
def assign_referral(referral_id: int, body: AssignRequest):
    if not mock_db.get_by_id(referral_id):
        raise HTTPException(404, f"Referral {referral_id} not found")
    return mock_db.update(referral_id, {"assigned_to": body.assigned_to})
 