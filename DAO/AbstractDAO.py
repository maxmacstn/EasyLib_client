class AbstractDAO(object):
    def __init__(self, server_ip="http://192.168.1.152:5000"):
        self.server_ip = server_ip