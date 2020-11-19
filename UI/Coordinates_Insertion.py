from base1 import engine, Session, Base
from Coordinates import Coordinates

def createPoint(X1, Y1, X2, Y2, location, userid):
    try:
        Base.metadata.create_all(engine)
        session = Session()
        print("coor")
        coordinate = Coordinates(X1, Y1, X2, Y2, location, userid)
        print("coor")
        session.add(coordinate)
        print("coor")
        session.commit()
        print("coor")
        session.close()
        if coordinate is not None:
            return "User Created"
    except ex:
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