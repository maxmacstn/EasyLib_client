from Scanner.Scanner import Scanner
from queue import Queue
import cv2
from pyzbar.pyzbar import decode


class CameraScanner(Scanner):
    def __init__(self,parent, width, height, fps, cam = 0):
        Scanner.__init__(self,parent)
        self.running = True
        self.imgQueue = Queue()
        self.cam = cam
        self.width = width
        self.height = height
        self.fps = fps

        # Initialize CV2 component
        self.capture = cv2.VideoCapture(cam)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.capture.set(cv2.CAP_PROP_FPS, fps)
        self.lastScannedData = None


    def run(self):
        while True:
            while self.running:
                frame = {}
                self.capture.grab()
                retval, img = self.capture.retrieve(0)
                frame["img"] = img
                if self.imgQueue.qsize() < 10:
                    self.imgQueue.put(frame)
                else:
                    pass

                try:
                    img_height, img_width, img_colors = img.shape
                except AttributeError:
                    # print("Camera scanner Attribute error")
                    continue
                scale_w = float(640) / float(img_width)
                scale_h = float(480) / float(img_height)
                scale = min([scale_w, scale_h])

                if scale == 0:
                    scale = 1
                img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                height, width, bpc = img.shape
                bpl = bpc * width
                decoded_data = decode(img)
                if decoded_data and decoded_data != self.lastScannedData:
                    scannedNum = str(decoded_data[0][0])[2:-1]
                    print("Barcode data : " + scannedNum)
                    self.parent.scannerCallback(scannedNum)


    def pause(self):
        print("Camera pause")
        self.running = False
        self.capture.release()


    def resume(self):
        print("Camera resume")
        self.capture = cv2.VideoCapture(self.cam)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_FPS, self.fps)
        self.running = True


    def getImageQueue(self):
        return self.imgQueue