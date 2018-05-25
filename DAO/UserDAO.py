import requests
from datetime import datetime
from constant import *
from DAO.AbstractDAO import AbstractDAO
from User.User import User



class UserDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent



    def getUserFromID(self, id):
        print("Get info id : " + str(id))
        try :
            path = '/user/' + str(id)
            response = requests.get(self.server_ip + path, timeout=self.timeout,
                                    headers=self.get_authentication_header(path))
            user = None
            if response.status_code == 200:   # Success
                user = self.constructUser(response.json())


        except requests.exceptions.ConnectionError:  # Connection timeout, use offline mockup data
            if self.parent is not None:
                self.parent.showError("Connection Error", "Please check your server connection.",1)
            return

        except Exception:  # Connection timeout, use offline mockup data
            if self.parent is not None:
                self.parent.showError("Connection Error", "Please check your server connection.",1)
            return




        if self.parent is not None:
            self.parent.login_callback(user)

        return user

    def getUserFromRFID_ID(self, rfid):
        try:
            path = '/user/rfid/' + str(rfid)
            response = requests.get(self.server_ip + path, timeout=self.timeout,
                                    headers=self.get_authentication_header(path))
            user = None
            if response.status_code == 200:     #Success
                user = self.constructUser(response.json())

        except Exception:  # Connection timeout, use offline mockup data
            if self.parent is not None:
                self.parent.showError("Connection Error", "Please check your server connection.", 1)
            return

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
