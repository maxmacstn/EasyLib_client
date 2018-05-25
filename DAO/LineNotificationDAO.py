from  DAO.AbstractDAO import AbstractDAO
import requests

class LineNotificationDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent



    def setToken(self, id,token):
        try :
            path = '/user/' + str(id) + "/token"
            response = requests.put(self.server_ip + path,json={"line_token": token}, timeout=self.timeout,
                                    headers=self.get_authentication_header(path))
            if response.status_code == 200:   # Success
                print("Success set line token")
                return True
            else:
                print("set token error " + response.text)
                return False
        except Exception:
            return False


    def notifyAllOnBorrow(self):
        try :

            path = '/manual_notification'
            response = requests.get(self.server_ip + path, timeout=self.timeout,
                                    headers=self.get_authentication_header(path))
            if response.status_code == 200:   # Success
                print("Success sent notification")
                return True
            else:
                print("sent error " + response.text)
                return False
        except Exception:
            return False