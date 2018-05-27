import os
import hmac
from datetime import datetime

class AbstractDAO(object):
    def __init__(self):
        # self.server_ip = 'http://' + os.environ['SERVER_IP']
        self.server_ip = 'http://137.116.140.178:8000'
        # self.server_ip = 'http://127.0.0.1:5000'
        self.timeout = 2

    @staticmethod
    def get_authentication_header(path, id=1):
        secret = os.environ['SECRET']

        timestamp = str(datetime.now().timestamp())

        hmac_encrypt = hmac.new(str.encode(secret), str.encode(path + '+' + timestamp), "sha3_256")

        return {"Authorization": "hmac " + str(id) + ":" + hmac_encrypt.hexdigest(),
                "Authorization-Timestamp": timestamp}