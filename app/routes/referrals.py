from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.models import Referral, ReferralCreate, ReferralUpdate, Status
from app import mock_db
 
router = APIRouter(prefix="/api/referrals", tags=["Referrals"])
 
 
@router.get("", response_model=List[Referral])
def list_referrals(status: Optional[Status] = None, assigned_to: Optional[str] = None):
    results = mock_db.get_all()
    if status:
        results = [r for r in results if r["status"] == status]
    if assigned_to:
        results = [r for r in results if r["assigned_to"] == assigned_to]
    return results
 
 
@router.get("/mine/{agent_name}", response_model=List[Referral])
def get_my_referrals(agent_name: str, status: Optional[Status] = None):
    results = [r for r in mock_db.get_all() if r["assigned_to"] == agent_name]
    if status:
        results = [r for r in results if r["status"] == status]
    if not results:
        raise HTTPException(404, f"No referrals found for '{agent_name}'")
    return results
 
 
@router.get("/{referral_id}", response_model=Referral)
def get_referral(referral_id: int):
    ref = mock_db.get_by_id(referral_id)
    if not ref:
        raise HTTPException(404, f"Referral {referral_id} not found")
    return ref
 
 
@router.post("", response_model=Referral, status_code=201)
def create_referral(body: ReferralCreate):
    return mock_db.insert(body.model_dump())
 
 
@router.patch("/{referral_id}", response_model=Referral)
def update_referral(referral_id: int, body: ReferralUpdate):
    if not mock_db.get_by_id(referral_id):
        raise HTTPException(404, f"Referral {referral_id} not found")
    return mock_db.update(referral_id, body.model_dump(exclude_none=True))
 
 
@router.patch("/{referral_id}/status", response_model=Referral)
def update_status(referral_id: int, status: Status):
    if not mock_db.get_by_id(referral_id):
        raise HTTPException(404, f"Referral {referral_id} not found")
    return mock_db.update(referral_id, {"status": status})
 
 
@router.delete("/{referral_id}", status_code=204)
def delete_referral(referral_id: int):
    if not mock_db.get_by_id(referral_id):
        raise HTTPException(404, f"Referral {referral_id} not found")
    mock_db.delete(referral_id)
 