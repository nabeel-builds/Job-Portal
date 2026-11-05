from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db, engine, Base
from app import models
from app.routers import auth, companies, jobs



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Portal API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}


app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(jobs.router)