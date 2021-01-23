# Zoomer-Bot
Bot to do your zoom for you so you can sleep and still leave the meeting :)
download either the py or ipynb (py should be faster and allows for multiprocessing)

Current assets folder is 1440p. 1080p and 4k users will probably need to generate their own assets
  - just take screenshots of the same buttons as are in current assets folder and replace the 1440p images.

required python libraries:
    pyautogui (pip install PyAutoGUI)
    pytesseract (pip install pytesseract)
    PIL (pip install Pillow)
    numpy (pip install numpy)
    pyvirtualcam (pip install pyvirtualcam)
    cv2 (pip install opencv-python)

other required programs:
tesseract.exe download:
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.0-alpha.20201127.exe (32 bit)
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe (64 bit)
  Downloads from UB Mannheim
    check for newer versions here: https://github.com/UB-Mannheim/tesseract/wiki

OBS:
https://obsproject.com/download
OBS virtual cam plugin:
https://github.com/Fenrirthviti/obs-virtual-cam/releases

pyvirtualcam setup:
You must register obs-virtualsource.dll in order for pyvirtualcam to open a virtual webcam
in cmd run:
  "regsvr32 /n /i:1 obs-virtualsource.dll" to register dll
  "regsvr32 /u obs-virtualsource.dll" to unregister dll
