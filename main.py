from mysql.insertUser import createUser, login,deleteUser

name = "Harvey Specter"
username = "harvey24"
email = "harvey@jtech.net"
password = "Jainam24"

# user = createUser(name, username, email, password)
# print(user)

token = login(username, email, password)

deleteUser(token)
