#used to controll the type of data api will accept and send out because 
#from frontend any type of unexpected data can come that dosent match our BaseClass written in models
#so for models/story.py
#we validate it here in schema/story.py

from typing import Optional,List,Dict
from datetime import datetime
from pydantic import BaseModel

class StoryOptionsSchema(BaseModel):
    text: str
    node_id :  Optional[int] = None

class StoryNodeBase(BaseModel):
    content:str
    is_ending:bool = False
    is_winning_ending: bool = False

class CompleteStoryNodeResponse(StoryNodeBase):
    id: int
    options: List[StoryOptionsSchema] = []

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None
    class Config:
        from_attributes = True

class CreateStory(BaseModel):
    theme : str
class CompleteStoryNodeResponse(StoryBase):
    id:int
    created_at: datetime
    root_node : CompleteStoryNodeResponse
    all_Nodes : Dict[int,CompleteStoryNodeResponse]
    
    class Config:
        from_attributes = True
    
