from sqlalchemy import Column, String, Integer, Date
#from base import Base
from base1 import Base, Session, engine
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username=Column(String(10),unique=True)
    email = Column(String(100), unique=True)
    password=Column(String(250))
    
    def __init__(self, name,username, email,password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
