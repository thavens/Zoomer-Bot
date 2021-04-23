import os
import secret
zoom_username = secret.user
zoom_password = secret.pass
thresh = 5 #this is at least how many people have to leave in 5 seconds to trigger logout
tesseract_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
zoom_path = os.path.expanduser('~') + '/AppData/Roaming/Zoom/bin/Zoom.exe' #path to zoom application
webcam = False
webcam_downscale_factor = 5 #i.e. enter 2 to display webcam at 1/2 resolution
video_file = 0 #path + file for virtual webcam recording. enter number to play real webcam. (default = 0)


#don't edit past tthis line
########################################################
loginID = None
password = None
url = None
