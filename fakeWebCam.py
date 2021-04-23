import pyvirtualcam
import numpy as np
import cv2

class Webcam:
    def __init__(self, video_file=0, downscale_factor=1):
        if(type(video_file).__name__ != 'int'):
            try:
                this.excam = cv2.VideoCapture(0)
            except:
                0
        self.cap = cv2.VideoCapture(video_file)
        if (self.cap.isOpened() == False):
            print("Error opening video  file")
            sys.stdout.flush()
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)//downscale_factor)
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//downscale_factor)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.cam = pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)

    def false_cam(self):
        while(True):
            while(self.cap.isOpened()):
                frame = np.zeros((self.cam.height, self.cam.width, 4), np.uint8) # RGBA
                ret, f = self.cap.read()
                frame[:,:,:3] = cv2.resize(f, (self.width, self.height), interpolation=None)
                if ret:
                    #data = np.apply_along_axis(a, -1, np.asarray(frame))
                    self.cam.send(frame)
                    self.cam.sleep_until_next_frame()
            cap = cv2.VideoCapture(video_name)

if __name__ == "__main__":
    cam = Webcam()
    print('Your false webcam seems to be working.')
    print('If you want to make sure go ahead and test out the virtual cam in a test zoom meeting.')
    cam.false_cam()
