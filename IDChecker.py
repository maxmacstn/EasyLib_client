import threading
import time


class IDChecker(threading.Thread):
    def __init__(self, parent, stuID):
        threading.Thread.__init__(self)
        self.id = stuID
        self.parent = parent

    def run(self):
        for i in range (101):
            self.parent.progressBar_loading.setValue(i)
            time.sleep(0.005)

        self.parent.login_callback(True)
