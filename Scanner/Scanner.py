import threading

'''
    An abstract class for scanning data from physical media to program
    
'''
class Scanner(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def run(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
