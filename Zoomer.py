#!/usr/bin/env python
# coding: utf-8

# In[10]:


import subprocess
import pyautogui
import sys
import os
import time
import pytesseract
from PIL import Image
import fakeWebCam
import webbrowser
import numpy as np
import numpy.ma as ma
import config

pytesseract.pytesseract.tesseract_cmd = config.tesseract_path


# In[4]:


print('''\033[36m
      /yyooooooooo++++++:-`
      :+ssssssssshhhhhhdddd-
                      -hddo
                    `sdds.
                   -hdh:
                 `+dds`
       ---------/hdd+ `.-.`        `--`    `.  .-.`  `.-.`          `:+++/-.          `-::::-`
       /yhhhhhddddy.:yhhyhhs/`  .oyhhyhyo. /hyhhyhhoohhyhho.      .sddhhhdddy-     .ddddddddddo
        ...-ydddh/`yho-   -shs`:hh/`  `/hh:/hh/` `ohho` `+hy.    oddy:    .hdd     -ddd:    .-`
         .sdddh/` :hy       hh:yh/      /hy+hy    `hh+    yh:   /ddddhyyyysddy     -dds
        :dddh/`   -hh-     -hh.ohs`    `sho/hs    `yh+    yh/   +ddo/+++++s+:`     :dd/
       +ddddossssshdhhs+:+shy- `+hho//ohh+`/hs    .hh+    yh/   `hdd/`             sdd:
       .sddddyooooo+`-/oso/-     `:+oo+/.  :o-     /o/    -o-    `+dddy+/:::/ss-   hdh`
                                                                    -+shhdddhyo`   ydo
                                                                                    `

                       .-////:-.`                               .ss.
                      -dddhhhddddho/`                           +dd.
                      `ddo    `.:oddh`                          +dd.
                      `ddo       `ydd.                          +dd.
                      `ddo  `.-/oddh-                      /++++hdds+++++`
                      `dddhddddddddy/`        .:++/-`      oyyyydddyyyyyy-
                      `dddhs+:.--/ohddo`    -yddhddddy+.        hdh
                      :ddo          /dds   :ddy-  `-+hddo       hdh
                      /dd:           ydd   sdd`       /dd/     .ddo
                      +dd-          /dd+   ydh:`    `:sdd/     .dd+
                      hdd/---.```./yddo    .odddhhhhddds-      .dd+
                      :shddddddddddds.        .:/+++:-         `/+`
                          ``------.
\033[0m''')
print('logging into zoom')

if not config.loginID is None:
    config.zoom_path = config.zoom_path.replace('\\', '/')
    print(config.zoom_path)
    try:
        subprocess.run([config.zoom_path])
    except:
        print('Cannot find Zoom.exe')
        print('Please make sure that zoom_path is correct!')
        #sys.exit()
    sys.exit()
    time.sleep(0.5)
    joinButton = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/join.png', grayscale=True, confidence=0.9)
    pyautogui.click(joinButton)
    time.sleep(0.5)
    pyautogui.typewrite(config.loginID + '\n')
    time.sleep(1)
    pyautogui.typewrite(config.password + '\n')
    loginButton = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/login.png', grayscale=True, confidence=0.9)
    pyautogui.click(loginButton)
    sys.exit()
else:
    try:
        webbrowser.open(config.url)
    except:
        print('url or browser did not work')
        sys.exit()
    try:
        time.sleep(1)
        openZoom = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/openZoom.png', grayscale=True, confidence=0.9)
        time.sleep(0.2)
        pyautogui.click(openZoom)
    except:
        try:
            time.sleep(5)
            openZoom = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/openZoom.png', grayscale=True, confidence=0.9)
            time.sleep(0.2)
            pyautogui.click(openZoom)
        except:
            print('did not prompt to open zoom')
    webbrowser.close()

video = fakeWebCam()
    
bgFound = None
while bgFound is None:
    bgFound = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/bg.png', grayscale=True, confidence=1)
    time.sleep(10)
pyautogui.click(bgFound)


# In[2]:


def startVideo():
    try:
        get_ipython().__class__.__name__
        from threading import Thread
        print('Warning: you are using a shell. For better speed use the interpreter.')
        x = Thread(target=video.falseCam, daemon=True)
    except:
        from multiprocessing import Process
        x = Process(target=video.falseCam, daemon=True)
    finally:
        x.start()
    
    time.sleep(3)
    video = pyautogui.locateOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    if video is None:
        pyautogui.press('alt')
        video = pyautogui.locateOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    pyautogui.click(video[0] + video[2], video[1])
    video = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/camName.png', grayscale=True, confidence=0.9)
    pyautogui.click(video)
    video = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    pyautogui.click(video)


# In[3]:


def breakout():
    #1. enter breakout if available
        #2. start loop to check for leave breakout
    breakout = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/breakoutJoin.png', grayscale=True, confidence=0.9)
    if breakout:
        print('entered breakout')
        pyautogui.click(breakout)
        while True():
            time.sleep(30)
            leaveBreakout = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/breakoutLeave.png', grayscale=True, confidence=0.9)
            if leaveBreakout:
                pyautogui.click(leaveBreakout)
                time.sleep(30)
                return True
    return False


# In[4]:


def userCount():
    #1. screenshot # of participants
    #2. turn completely black and white
    #3. save image as cap.png
    #4. use tesseract to turn image to int
    #5. return int value of participants
    participantsLocation = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/participants.png', grayscale=True, confidence = 0.8)
    if participantsLocation is None:
        pyautogui.press('alt')
        participantsLocation = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/participants.png', grayscale=True, confidence = 0.8)
    people = pyautogui.screenshot()
    people = people.crop((participantsLocation.x,
                         participantsLocation.y-30,
                         participantsLocation.x + 30,
                         participantsLocation.y))
    
    data = np.asarray(people)
    a = lambda a: int(np.mean(a))
    data = np.apply_along_axis(a, -1, data)
    data[ma.masked_greater(data, 130).mask] = 255
    data[ma.masked_less_equal(data, 130).mask] = 0
    data = 255 - data
    data = data.flatten()
    img = np.array([])
    for i in data:
        img = np.append(img, np.array([i, i, i], dtype=np.int32))
    img = np.reshape(img, (30,30,3))
    img = img.astype(np.uint8)
    people = Image.fromarray(img)
    people = people.resize((300, 300), Image.BILINEAR)
    people.save(os.getcwd() + '/assets/cap.png')
    
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 7 digits')
    #text = text[:text.index('\n')]
    text = text.strip()
    return int(text)


# In[5]:


def leave():
    #click leave and confirm leave
    print('leaving meeting')
    leave = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/leave.png', grayscale=True, confidence=0.9)
    if leave is None:
        pyautogui.press('alt')
        leave = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/leave.png', grayscale=True, confidence=0.9)
    pyautogui.click(leave)
    leave = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/leaveConfirm.png', grayscale=True, confidence=0.9)
    pyautogui.click(leave)


# In[13]:


if __name__ == '__main__':
    if config.webcam:
        startVideo()
    old = None
    while True:
        time.sleep(5)
        if breakout():
            old = None
        count = userCount()
        print(count, 'users')
        if old != None and old - count > config.thresh:
            print('Users leaving')
            leave()
            break
        old = count


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




