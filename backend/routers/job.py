from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import session
from db.database import get_db
from models.job import StoryJob
from schemas.job import StoryJobresponse

router  = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/{job_id}", response_model = StoryJobresponse)
def get_job_status(job_id: str, db: session = Depends(get_db)):
    job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="job not found")

    return job