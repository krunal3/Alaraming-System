import bcrypt
from sqlalchemy import update
import jwt
#import Users
#import base
from base1 import Base,Session, engine
from Users1 import User
def createUser(name, username, email, password):
    try:
        Base.metadata.create_all(engine)
        session = Session()
        hashandsalt = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = Users.User(name, username, email, hashandsalt)
        session.add(user)
        session.commit()
        session.close()
        if user is not None:
            return "User Created"
    except NameError:
        return "Error"
    #except expression as identifier:
#      return "Some Error Occured"


def login(username, email, password):
    try:
        Base.metadata.create_all(engine)
        session = Session()
        user = session.query(User)\
            .filter(User.username == username and User.email == email)\
            .all()
        if (len(user) == 0):
            return "NO User Found"
        valid = bcrypt.checkpw(password.encode(), user[0].password.encode())
        if (valid):
            token = jwt.encode(
                {'userid': user[0].id,
                 'email': user[0].email}, "jtechsecret"
            )
            session.close()
            return token
        else:
            return "User Not Found"
    except NameError:
        print("Error Occured!!")

# Find the way of Updating users 
# def updateUser(name, username, email, password,token):
#     try:
#         data = jwt.decode(token, "jtechsecret")
#         if (data == None):
#             return "Not Authenticated"
#         Base.metadata.create_all(engine)
#         session = Session()

#     except expression as identifier:
#         pass


def deleteUser(token):
    try:
        data = jwt.decode(token, "jtechsecret")
        if (data == None):
            return "Not Authenticated"
        Base.metadata.create_all(engine)
        session = Session()
        deletedUser = session.query(User)\
            .filter(User.id == data['userid'])\
            .delete()
        print(deleteUser)
        session.commit()
        session.close()
        return "User Deleted"
    except:
        return "Some Error Occured"

