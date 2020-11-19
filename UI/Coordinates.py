from sqlalchemy import Column, String, Integer, Date
from base1 import Base

class Coordinates(Base):
    __tablename__ = "Coordinates"
    
    id = Column(Integer, primary_key=True)
    X1 = Column(Integer)
    Y1 = Column(Integer)
    X2 = Column(Integer)
    Y2 = Column(Integer)
    location = Column(String(100))
    userid = Column(Integer)
    
    def __init__(self,X1 ,Y1 ,X2 ,Y2 ,location,userid):
        self.X1=X1
        self.Y1=Y1
        self.X2=X2
        self.Y2=Y2
        self.location=location
        self.userid=userid

