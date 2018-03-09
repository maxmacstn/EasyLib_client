from queue import Queue
import cv2
import threading


class CameraCapture(threading.Thread):
    def __init__(self, cam, width, height, fps):
        threading.Thread.__init__(self)
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
                    # print(queue.qsize())
                    pass

    def pause(self):
        self.running = False
        self.capture.release()

    def resume(self):
        self.capture = cv2.VideoCapture(self.cam)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_FPS, self.fps)
        self.running = True



    def getImageQueue(self):
        return self.imgQueue
