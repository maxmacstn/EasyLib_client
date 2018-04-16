class Student:
    def __init__(self,id,fname, lname,lineToken = None):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.lineToken  = lineToken

    def getName(self):
        return self.fname +" " + self.lname

    def getID(self):
        return self.id

    def getLineNotifyToken(self):
        return self.lineToken

    def setLineNotifyToken(self,token):
        self.lineToken = token