from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
 
# מדביקים את ה-connection string מ-Neon (או כל Postgres אחר)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host/dbname")
 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
 
 
def get_db():
    """מחזיר session למסד הנתונים — נסגר אוטומטית בסוף הבקשה."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 