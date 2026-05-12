from fastapi import FastAPI
from app.database import Base, engine
from app.routes import referrals, assignments
 
# יוצר את הטבלאות במסד הנתונים אוטומטית בהרצה הראשונה
Base.metadata.create_all(bind=engine)
 
app = FastAPI(title="Referrals API", version="1.0.0")
 
app.include_router(referrals.router)
app.include_router(assignments.router)
 