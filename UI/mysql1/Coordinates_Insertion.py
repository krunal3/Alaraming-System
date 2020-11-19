from base import engine, Session, Base
from Coordinates import Coordinates

def createPoint(X, Y, location, userid):
    try:
        Base.metadata.create_all(engine)
        session = Session()
        coordinate = Coordinates(X, Y, location, userid)
        session.add(coordinate)
        session.commit()
        session.close()
        return coordinate
    except:
        return "Some Error Occured"

def deletePoint(id):
    try:
        Base.metadata.create_all(engine)
        session = Session()
        deletedPoint = session.query(Coordinates)\
            .filter(Coordinates.id == id)\
            .delete()
        session.commit()
        session.close()
  #  except expression as identifier:
   #     pass
    except NameError:
        return "Error"