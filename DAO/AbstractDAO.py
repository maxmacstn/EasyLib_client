class AbstractDAO(object):
    # def __init__(self, server_ip="http://127.0.0.1:5000"):
    def __init__(self, server_ip="http://137.116.140.178:8000/"):
        self.server_ip = server_ip
        self.timeout = 2