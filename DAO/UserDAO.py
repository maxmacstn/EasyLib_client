from User.Student import Student
import time
import requests
from datetime import datetime
from constant import *

from DAO.AbstractDAO import AbstractDAO
from User.User import User


# Non-server test
#
# class UserDAO:
#     def __init__(self,parent = None, serverIP = "10.0.0.1"):
#         self.ip = serverIP
#         self.parent = parent
#
#
#     def getUserFromID(self, id):
#         # Fake loading
#         time.sleep(0.5)
#
#         if (id == "59090030"):
#             self.parent.login_callback(Student(59090030,"Sitinut","Waisara","ycrnAC5g1ekyjeF925i0gNbZQMuZWQ2MkIjIEzYBsZ3"))
#
#         else:
#             self.parent.login_callback(None)
#
#     def getUserFromRFID_ID(self, rfid_id):
#         # Fake loading
#         time.sleep(0.5)
#
#         if (rfid_id == "f3e09a4f"):
#             self.parent.login_callback(Student(59090030,"Sitinut","Waisara","ycrnAC5g1ekyjeF925i0gNbZQMuZWQ2MkIjIEzYBsZ3"))
#         else:
#             self.parent.login_callback(None)



# class UserDAO(AbstractDAO):
#     def __init__(self, parent = None):
#         AbstractDAO.__init__(self)
#         self.parent = parent
#
#
#     def getUserFromID(self, id):
#         print("Get info id : " + str(id))
#         response = requests.get(self.server_ip + '/user/' + str(id))
#
#         user = self.constructUser(response.json())
#
#         if self.parent is not None:
#             self.parent.login_callback(user)
#
#         return user
#
#     def getUserFromRFID_ID(self, rfid):
#         response = requests.get(self.server_ip + '/user/rfid/' + str(rfid))
#
#         user = self.constructUser(response.json())
#
#         if self.parent is not None:
#             self.parent.login_callback(user)
#
#         self.parent.login_callback(user)
#         return user
#
#     @staticmethod
#     def constructUser(arguments):
#         arguments['registered_on'] = datetime.strptime(arguments['registered_on'], rfc_822_format)
#
#         return User(**arguments)
#
# if __name__ == "__main__":
#     userDAO = UserDAO()
#     print(userDAO.getUserFromID(1).name)


class UserDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def getUserFromID(self, id):
        print("Get info id : " + str(id))
        response = requests.get(self.server_ip + '/user/' + str(id))
        user = None

        if response.status_code == 200:
            user = self.constructUser(response.json())

        if self.parent is not None:
            self.parent.login_callback(user)

        return user

    def getUserFromRFID_ID(self, rfid):
        response = requests.get(self.server_ip + '/user/rfid/' + str(rfid))
        user = None
        if response.status_code == 200:
            user = self.constructUser(response.json())

        if self.parent is not None:
            self.parent.login_callback(user)

        return user

    @staticmethod
    def constructUser(arguments):
        if arguments == None:
            return None

        time_arg = "registered_on"

        arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        return User(**arguments)


if __name__ == "__main__":
    userDAO = UserDAO()
    print(userDAO.getUserFromID(1).name)
