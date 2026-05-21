from fastapi import FastAPI
from app.routes import referrals, assignments
 
app = FastAPI(title="Referrals API", version="1.0.0")
 
app.include_router(referrals.router)
app.include_router(assignments.router)
 