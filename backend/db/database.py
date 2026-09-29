from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings

engine = create_engine(
    #.env se config me type validation fir yaha engine banega sqlalchemy ka for connect hoga alchemy DB se 
    #yaha settings se import kara hai kyuki core/config me settings naam ka function hai joki type validation karra hai 
    settings.DATABASE_URL
)

sessionLocal = sessionmaker(autocommit = False, autoflush=False,bind = engine)
#"This Python class is a database model, and you should keep track of it as a table."
#Think of Base as the parent class for all your SQLAlchemy models.
#from here it will bw imported to models
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_table():
    Base.metadata.create_all(bind=engine)