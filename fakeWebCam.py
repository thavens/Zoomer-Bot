#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyvirtualcam
import numpy as np
import cv2
import time
import config


# In[ ]:


def __init__(self):
    self.cap = cv2.VideoCapture(config.video_file)
    if (cap.isOpened()== False):  
        print("Error opening video  file")
    self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)//config.webcam_downscale_factor)
    self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//config.webcam_downscale_factor)
    self.fps = self.cap.get(cv2.CAP_PROP_FPS)
    self.cam = pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps, delay=50)
    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)


# In[2]:


def falseCam(self):
    while(True):
        while(self.cap.isOpened()):
            frame = np.zeros((cam.height, cam.width, 4), np.uint8) # RGBA
            ret, f = cap.read()
            frame[:,:,:3] = cv2.resize(f, (self.width, self.height), interpolation=None)
            if ret:
                #data = np.apply_along_axis(a, -1, np.asarray(frame))
                self.cam.send(frame)
                self.cam.sleep_until_next_frame()
        cap = cv2.VideoCapture(video_name)


# In[3]:


#'D:\Recordings\FaceRecording.mp4'
if __name__ == "__main__":
    falseCam(0)
    print('tf you running this for?!')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




