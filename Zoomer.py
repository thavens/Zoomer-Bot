#!/usr/bin/env python
# coding: utf-8

# In[61]:


from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
import config
import win32gui
import multiprocessing
from fakeWebCam import Webcam


# In[34]:


#starts selenium will mic and webcam perms enabled and logs into zoom
#signs into zoom online
def open():
    options = Options()
    options.add_experimental_option("prefs", {     "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "download_restrictions": 3
  })
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    driver.get('https://fuhsd-org.zoom.us/signin')
    elem = driver.find_element_by_xpath('//*[@id="identifierId"]')
    elem.send_keys(config.zoom_username + '\n')
    while(True):
        try:
            elem = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
            elem.send_keys(config.zoom_password + '\n')
        except:
            time.sleep(1)
        else:
            break
    time.sleep(3)
    return driver

#enters to zoom link or enters the zoom login id into zoom.us/join
def prep_meeting(config, meeting):
    if config.webcam:
        start_cam()
    if config.url:
        meeting.get(config.url)
    elif config.loginID:
        meeting.get('https://zoom.us/j')
        elem = meeting.find_element_by_xpath('//*[@id="join-confno"]')
        elem.send_keys(link + '\n')
    else:
        raise ValueError()


# In[6]:


#uses threading or multiprocessing to startup pyvirtual cam and stream video/capture through to zoom
def start_cam():
    video = Webcam()
    try:
        get_ipython() #throws error if not ipython
        from threading import Thread #ipythons does not work with multiprocessing
        print('Warning: you are using a shell. For better speed use the interpreter.')
        x = Thread(target=video.false_cam, daemon=True)
    except:
        from multiprocessing import Process #multiprocessing is faster but only works in interp.
        x = Process(target=video.false_cam, daemon=True)
    finally:
        x.start()


# In[2]:


# cancels alert to open the zoom app if downloaded.
#    note: selenium is not able to close alert because while it looks like a js alert it is in fact not
# opens zoom meeting with webbrowser client
# mutes mic by default and disables webcam if not enabled in config
def enter_meeting(meeting):
    def cancel():
        cancel = None
        while cancel is None:
            cancel = pyautogui.locateOnScreen('./assets/Cancel.png', grayscale=True, confidence=.8)
            time.sleep(1)
        if cancel:
            pyautogui.click(cancel)
    
    cancel()
    try:
        meeting.find_element_by_xpath('//*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3[2]/a').click()
    except:
        xpath = '//*[@id="zoom-ui-frame"]/div[2]/div/div[1]/div'
        elem = WebDriverWait(meeting, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
        elem.click()
        cancel()
        meeting.find_element_by_xpath('//*[@id="zoom-ui-frame"]/div[2]/div/div[2]/h3[2]/a').click()
    if not config.webcam:
        meeting.find_element_by_xpath('//*[@id="video-icon"]').click()
    meeting.find_element_by_xpath('//*[@id="mic-icon"]').click()
    meeting.find_element_by_xpath('//*[@id="joinBtn"]').click()


# In[4]:


# enters passcode if required
# continually checks participant count to make sure to quit out of class on time
# makes webdriver quit to exit meeting
def maintain_meeting(config, meeting):
    try:
        time.sleep(2)
        elem = meeting.find_element_by_xpath('//*[@id="inputpasscode"]')
        elem.send_keys(config.password + '\n')
        print('Meeting passcode entered')
    except:
        print('No meeting password was needed')
    xpath = '//*[@id="wc-footer"]/div/div[2]/button[1]/div/div/span/span'
    while True:
        try:
            elem = WebDriverWait(meeting, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
            break
        except:
            print('Could not get participant count element')
    count = int(elem.get_attribute('innerHTML'))
    old = count;
    while(count + config.thresh > old):
        print('Participants:', count)
        old = count
        time.sleep(5)
        count = int(elem.get_attribute('innerHTML'))
    meeting.quit()
    print('Meeting complete!')


# In[58]:


#reassigns chrome driver's default webcam to OBS-camera
#enables the use of virtual cam
def default_webcam(meeting):
    if not config.webcam:
        return
    meeting.get('chrome://settings/content/camera')
    hwnd = win32gui.FindWindow(None, 'Settings - Camera - Google Chrome')
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(1)
    loc = pyautogui.locateOnScreen('./assets/DropDown.png', grayscale=True, confidence=.8)
    pyautogui.click(loc)
    loc = pyautogui.locateOnScreen('./assets/OBS-camera.png' grayscale=True, confidence=0.9)
    pyautogui.click(loc)


# In[35]:


def start(config):
    meeting = open()
    default_webcam(meeting)
    prep_meeting(config, meeting)
    enter_meeting(meeting)
    maintain_meeting(config, meeting)


# In[1]:


if __name__ == '__main__':
    #config.url = insert test zoom link
    #config.password = or zoom meeting password
    #config.loginID = and zoom id
    config.video_file = 'ex'
    start(config)
    

