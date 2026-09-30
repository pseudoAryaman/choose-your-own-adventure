#used to controll the type of data api will accept and send out because 
#from frontend any type of unexpected data can come that dosent match our BaseClass written in models
#so for models/story.py
#we validate it here in schema/story.py

from typing import Optional,List,Dict
from datetime import datetime
from pydantic import BaseModel

