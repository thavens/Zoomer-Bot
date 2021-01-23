import subprocess
import pyautogui
import sys
import os
import time
import pytesseract
from PIL import Image
import webbrowser
import numpy as np
import numpy.ma as ma
from fakeWebCam import Webcam
import pyvirtualcam
from PIL import ImageFilter, ImageEnhance
import win32gui

def startVideo(config):
    x = None
    video = Webcam(config.video_file, config.webcam_downscale_factor)
    try:
        #get_ipython().__class__.__name__
        from threading import Thread
        print('Warning: you are using a shell. For better speed use the interpreter.')
        x = Thread(target=video.false_cam, daemon=True)
    except:
        from multiprocessing import Process
        x = Process(target=video.false_cam, daemon=True)
    finally:
        x.start()

    time.sleep(2)
    video = pyautogui.locateOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    if video is None:
        pyautogui.press('alt')
        video = pyautogui.locateOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    pyautogui.click(video[0] + video[2], video[1])
    video = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/camName.png', grayscale=True, confidence=0.9)
    pyautogui.click(video)
    video = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/startVideo.png', grayscale=True, confidence=0.9)
    pyautogui.click(video)

def breakout():
    #1. enter breakout if available
        #1. start loop to check for leave breakout
    #(not implemented) 2. check if automatically inserted into breakout
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

def userCount():
    #1. screenshot # of participants
    #2. turn completely black and white
    #4. upscale with antialiasing
    #5. apply sky high contrast
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
    #people = people.resize((300, 300), Image.BICUBIC)
    #ret, thresh = cv2.threshold(np.asarray(people), 127, 255, cv2.THRESH_BINARY)
    #kernel = np.ones((3,3),np.uint8)
    #people = cv2.erode(thresh,kernel,iterations = 1)
    enhancer = ImageEnhance.Contrast(people)
    people = enhancer.enhance(10)
    people.save(os.getcwd() + '/assets/cap.png')

    text = pytesseract.image_to_string(people, lang='eng', config='--psm 7 digits')
    try:
        #text = text[:text.index('\n')]
        text = text.strip()
    except:
        print('could not convert to into. value:', text)

    print('users:', text)
    return int(text)

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

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def start(config):
    print('id:', config.loginID)
    print('url:', config.url)
    pytesseract.pytesseract.tesseract_cmd = config.tesseract_path
    #opening zoom and joining class
    print('logging into zoom')

    if not config.loginID is None:
        config.zoom_path = config.zoom_path.replace('\\', '/')
        print(config.zoom_path)
        try:
            subprocess.run([config.zoom_path])
        except:
            print('Cannot find Zoom.exe')
            print('Please make sure that zoom_path is correct!')
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
    elif not config.url is None:
        try:
            webbrowser.open(config.url)
        except:
            print('\033[31;1m# ERROR: url or browser did not work\033[0m')
            sys.exit()

        time.sleep(2)
        openZoom = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/openZoom.png', grayscale=True, confidence=0.9)
        if openZoom is None:
            time.sleep(5)
            openZoom = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/openZoom.png', grayscale=True, confidence=0.9)
        time.sleep(0.2)
        pyautogui.click(openZoom)
    else:
        print('\033[31;1m# ERROR: no login ID or link was provided\033[0m')
        sys.exit()
    
    #bgFound = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/bg.png', grayscale=True, confidence=0.95)
    #while bgFound is None:
    #    print('locating')
    #    bgFound = pyautogui.locateCenterOnScreen(os.getcwd() + '/assets/bg.png', grayscale=True, confidence=0.95)
    #    time.sleep(10)
    #pyautogui.click(bgFound)

    while True:
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        for i in top_windows:
            if "zoom meeting" in i[1].lower():
                print(i)
                win32gui.ShowWindow(i[0],5)
                win32gui.SetForegroundWindow(i[0])
                break
        else:
            time.sleep(10)
            continue
        break

    #main loop
    ############################################################################
    if config.webcam:
        startVideo(config)
    old = None
    while True:
        time.sleep(5)
        if breakout():
            old = None
        count = userCount()
        print(count, 'users')
        if old != None and old - count > config.thresh:
            print('Users leaving')
            #leave()
            break
        old = count
