#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyvirtualcam
import numpy as np
import cv2
import time


# In[2]:


def falseCam():
    cap = cv2.VideoCapture(config.video_file)
    if (cap.isOpened()== False):  
        print("Error opening video  file")
    a = lambda a: np.append(a, [1])
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)//config.webcam_downscale_factor)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//config.webcam_downscale_factor)
    print((width, height))
    fps = cap.get(cv2.CAP_PROP_FPS)
    with pyvirtualcam.Camera(width=width, height=height, fps=fps, delay=50) as cam:
        while(cap.isOpened()):
            frame = np.zeros((cam.height, cam.width, 4), np.uint8) # RGBA
            ret, f = cap.read()
            frame[:,:,:3] = cv2.resize (f, (width, height), interpolation=None)
            if ret:
                #data = np.apply_along_axis(a, -1, np.asarray(frame))
                cam.send(frame)
                cam.sleep_until_next_frame()


# In[3]:


#'D:\Recordings\FaceRecording.mp4'
if __name__ == "__main__":
    falseCam(0)
    print('tf you running this for?!')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




