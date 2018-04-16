import threading
from queue import Queue
from serial import Serial

SERIAL_PORT = "COM11"

class RFIDScanner(threading.Thread):
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.queue = Queue()
        self.running = True

        # Init serial connection
        self.ser = Serial(SERIAL_PORT, 9600)



    def run(self):
        """
                This is where we handle the asynchronous I/O.
        """
        while 1:
            while self.running:
                # This is where we poll the Serial port.
                # time.sleep(rand.random() * 0.3)
                # msg = rand.random()
                # self.queue.put(msg)
                msg = self.ser.readline();
                decode_message = msg.decode('utf-8').strip()
                if (msg and len(decode_message) >1):
                    if(decode_message == "RFID Reader is ready.."):
                        continue
                    print("Data " + decode_message + "..")
                    self.parent.scannerCallback(decode_message,1)

                else:
                    pass

        self.ser.close()

    def pause(self):
        self.running = False

    def resume(self):
        self.running = True
