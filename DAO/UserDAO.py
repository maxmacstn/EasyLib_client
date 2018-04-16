from User.Student import Student
import time

class UserDAO:
    def __init__(self,parent = None, serverIP = "10.0.0.1"):
        self.ip = serverIP
        self.parent = parent


    def getUserFromID(self, id):
        # Fake loading
        time.sleep(0.5)

        if (id == "59090030"):
            self.parent.login_callback(Student(59090030,"Sitinut","Waisara","ycrnAC5g1ekyjeF925i0gNbZQMuZWQ2MkIjIEzYBsZ3"))

        else:
            self.parent.login_callback(None)

    def getUserFromRFID_ID(self, rfid_id):
        # Fake loading
        time.sleep(0.5)

        if (rfid_id == "f3e09a4f"):
            self.parent.login_callback(Student(59090030,"Sitinut","Waisara","ycrnAC5g1ekyjeF925i0gNbZQMuZWQ2MkIjIEzYBsZ3"))
        else:
            self.parent.login_callback(None)
