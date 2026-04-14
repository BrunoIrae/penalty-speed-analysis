import cv2

class VideoProcessor:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()