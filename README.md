# Zoomer-Bot
Bot to do your zoom for you so you can sleep and still leave the meeting :)

Current assets folder is 1440p. 1080p and 4k users will probably need to generate their own assets
  - just take screenshots of the same buttons as are in current assets folder and replace the 1440p images.

# Steps:
- clone repo
- edit timetable.txt and config.py
- run Zoomer.py

required python libraries:
    pyautogui (pip install PyAutoGUI)
    selenium (pip install selenium)
    PIL (pip install Pillow)
    numpy (pip install numpy)
    pyvirtualcam (pip install pyvirtualcam)
    cv2 (pip install opencv-python)

Pyvirtual cam is only required in the case that you want to stream a prerecorded video as a virtual webcam.
# OBS:
https://obsproject.com/download
OBS virtual cam plugin:
https://github.com/Fenrirthviti/obs-virtual-cam/releases

# pyvirtualcam setup:
You must register obs-virtualsource.dll in order for pyvirtualcam to open a virtual webcam
in cmd run:
  "regsvr32 /n /i:1 obs-virtualsource.dll" to register dll
  "regsvr32 /u obs-virtualsource.dll" to unregister dll
