import uuid 
from typing import Optional
from datetime import datetime
from fastapi import APIRouter,Depends,HTTPException,Cookie,Response,BackgroundTasks
from sqlalchemy.orm import Session
from db.database import get_db, sessionLocal 
#    |
#    |
#    v
#A route can use it like this:
# @router.get("/")def get_stories(db: Session = Depends(get_db)):    ...



# Read that as:
# FastAPI, call get_db(), provide the yielded database session as db, and close it when the request's dependency lifecycle finishes.

# This avoids manually creating and closing a database session in every route.
# sessionLocal
# from db.database import get_db, sessionLocal



# This imports the session factory directly. It can be useful for code that needs to create its own session outside the normal request dependency, such as some background jobs.
# However, if you don't use sessionLocal anywhere in this file, you can remove that import.
# Also, the conventional name is SessionLocal, with a capital S.
from models.story import Story,StoryNode
from models.job import StoryJob
from schemas.story import(CompleteStoryNodeResponse, CompleteStoryResponse,CreateStoryRequest)

from schemas.job import StoryJobresponse

router = APIRouter(
    prefix="/stories",
    tags=["stories"] #to document in swagger /docs as stories 
)
#A session ID doesn't necessarily track how long someone has been on the website.
# A session ID identifies a browser's session or visitor context, allowing your application to associate multiple requests with the same visitor.
# Here's the function you started writing:

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create",response_model = StoryJobresponse)
def create_story(
    request: CreateStoryRequest,
    background_Task: BackgroundTasks,
    response: Response,
    #depends keyword used for creating dependency for example here depends is used because we need to get the session id from the function get_session_id first to assign the id to the argument in the function.
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key= "session_id", value=session_id, httponly=True)
    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id= job_id,
        session_id = session_id,
        theme = request.theme,
        status = "pending"
    )
    db.add(job)
    db.commit()

    background_Task.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job

def generate_story_task(job_id: str, theme:str, session_id:str):
    db = sessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return 
        try:
            job.status = "processing"
            db.commit()
            Story={} #TODO: generate story

            job.story_id = 1
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()

@router.get("/{story_id}/completed", response_model = CompleteStoryNodeResponse)
def get_completed_story(story_id: int,db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail = "story bnale bhai")

    completed_story = build_complete_story_tree(db,story)
    return completed_story

#this function will comvert the retrieved story(from the db) to a readable format which the frontend can read
def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    pass

        

