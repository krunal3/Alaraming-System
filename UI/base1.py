from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://krunal:1234@localhost:3306/MCTE')

Session = sessionmaker(bind=engine)

Base = declarative_base()
