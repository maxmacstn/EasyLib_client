class User:
    def __init__(self, id, name, registered_on, email, is_active, lineToken = None):
        self.id = id
        self.name = name
        self.lineToken  = lineToken
        self.registered_on = registered_on
        self.email = email
        self.is_active = is_active

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def getLineNotifyToken(self):
        return self.lineToken

    def setLineNotifyToken(self,token):
        self.lineToken = token