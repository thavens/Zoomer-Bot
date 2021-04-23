#!/usr/bin/env python
# coding: utf-8

# In[147]:


from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pyautogui
import config


def open():
    options = Options()
    options.add_experimental_option("prefs", {     "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "download_restrictions": 3
  })
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    driver.get('https://fuhsd-org.zoom.us/signin')
    elem = driver.find_element_by_xpath('//*[@id="identifierId"]')
    elem.send_keys(config.zoom_username)
    while(True):
        try:
            elem = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
            elem.send_keys(config.zoom_password)
        except:
            time.sleep(1)
        else:
            break
    time.sleep(3)
    return driver

def prep_meeting(config):
    driver = open()
    driver.get('https://us04web.zoom.us/j/4949655895')
    if config.url:
        driver.get(config.url)
    elif config.loginID:
        driver.get('https://zoom.us/j')
        elem = driver.find_element_by_xpath('//*[@id="join-confno"]')
        elem.send_keys(link + '\n')
    else:
        raise ValueError()
    return driver


# In[149]:


def enter_meeting(meeting):
    def cancel():
        cancel = None
        while cancel is None:
            cancel = pyautogui.locateOnScreen('./assets/Cancel.png', grayscale=True, confidence=.8)
            time.sleep(1)
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
    meeting.find_element_by_xpath('//*[@id="video-icon"]').click()
    meeting.find_element_by_xpath('//*[@id="mic-icon"]').click()
    elem = meeting.find_element_by_xpath('//*[@id="joinBtn"]')
    elem.click()


# In[153]:


def maintain_meeting(config):
    try:
        time.sleep(2)
        elem = meeting.find_element_by_xpath('//*[@id="inputpasscode"]')
        elem.send_keys(config.password + '\n')
    except:
        0
    xpath = '//*[@id="wc-footer"]/div/div[2]/button[1]/div/div/span/span'
    elem = WebDriverWait(meeting, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
    count = int(elem.get_attribute('innerHTML'))
    old = count;
    while(count + config.thresh > old):
        print('Participants:', count)
        old = count
        time.sleep(5)
        count = int(elem.get_attribute('innerHTML'))
    meeting.quit()


# In[157]:


def start(config):
    meeting = prep_meeting(config)
    enter_meeting(meeting)
    maintain_meeting(meeting)


# In[ ]:


if __name__ == '__main__':
    config.url = #insert test zoom link
    start(config)
