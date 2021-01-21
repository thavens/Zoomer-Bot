#!/usr/bin/env python
# coding: utf-8

# In[6]:


import subprocess
import pyautogui
import sys
import os
import time
import pytesseract
from PIL import Image
import numpy as np
import numpy.ma as ma
import fakeWebCam

loginID = '725 405 7950'
password = '140287'
thresh = 5 #how many or more people have to leave in 5 seconds to trigger logout


# In[ ]:


print('logging into zoom')
result = subprocess.run(['C:/Users/micha/AppData/Roaming/Zoom/bin/Zoom.exe'])
time.sleep(0.5)
joinButton = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/join.png', grayscale=True, confidence=0.9)
pyautogui.click(joinButton)
time.sleep(0.5)
pyautogui.typewrite(loginID + '\n')
time.sleep(1)
pyautogui.typewrite(password + '\n')
loginButton = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/login.png', grayscale=True, confidence=0.9)
pyautogui.click(loginButton)

bgFound = None
while bgFound == None:
    bgFound = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/bg.png', grayscale=True, confidence=1)
    time.sleep(10)
pyautogui.click(bgFound)


# In[2]:


def startVideo():
    try:
        shell = get_ipython().__class__.__name__
    x = threading.Thread(target=fakeWebCam.falseCam, args=(), daemon=True)
    x.start()
    time.sleep(3)
    video = pyautogui.locateOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    if video == None:
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
        print('breakout')
        pyautogui.click(breakout)
        while True():
            time.sleep(30)
            leaveBreakout = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/breakoutLeave.png', grayscale=True, confidence=0.9)
            if leaveBreakout:
                pyautogui.click(leaveBreakout)
                time.sleep(30)
                return True
    print('no breakout')
    return False


# In[4]:


def userCount():
    #1. screenshot # of participants
    #2. turn completely black and white
    #3. save image as cap.png
    #4. use tesseract to turn image to int
    #5. return int value of participants
    participantsLocation = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/participants.png', grayscale=True, confidence = 0.8)
    if participantsLocation == None:
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
    
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    text = pytesseract.image_to_string(img, lang='eng', config='--psm 7 digits')
    text = text[:text.index('\n')]
    return int(text)


# In[8]:


def leave():
    #click leave and confirm leave
    print('leaving meeting')
    leave = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/leave.png', grayscale=True, confidence=0.9)
    if leave == None:
        pyautogui.press('alt')
        leave = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/leave.png', grayscale=True, confidence=0.9)
    pyautogui.click(leave)
    leave = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/leaveConfirm.png', grayscale=True, confidence=0.9)
    pyautogui.click(leave)


# In[10]:


if __name__ == '__main__':
    startVideo()
    old = None
    while True:
        time.sleep(5)
        if breakout():
            old = None
        count = userCount()
        print(count, 'users')
        if old != None and old - count > thresh:
            print('Users leaving')
            leave()
        old = count


# In[ ]:




