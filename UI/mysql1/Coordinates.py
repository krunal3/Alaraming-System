from sqlalchemy import Column, String, Integer, Date
from base import Base

class Coordinates:
    __tablename__ = "Coordinates"
    
    id = Column(Integer, primary_key=True)
    X = Column(Integer)
    Y = complex(Integer)
    location = Column(String(100))
    userid = Column(Integer)
    
    def __init__(self,X,Y,location,userid):
        self.X=X
        self.Y=Y
        self.location=location
        self.userid=userid

