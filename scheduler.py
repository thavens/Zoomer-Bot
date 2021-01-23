import time as sleep
from datetime import datetime
import numpy as np
import config
import Zoomer
import os
import inhibit_sleep
import atexit

#required for text coloring to work

def on_exit():
    inhibit_sleep.uninhibit()

os.system('')
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
print('\u001b[33m# WARNING: Please make sure that you have tested your fakeWebCam before starting.\033[0m')
if not os.path.exists(config.tesseract_path):
    print('There is something wrong with your tesseract path')
    sys.exit()
elif not os.path.exists(config.zoom_path):
    print('There is something wrong with your zoom path')
    sys.exit()

print('Tesseract file found')
print('Zoom app found')
atexit.register(on_exit)
inhibit_sleep.inhibit()

print('Intializing class times')
times = list()
logins = list()
with open('timetable.txt') as f:
    while True:
        line = f.readline()
        if '######' in line:
            break
    while True:
        line = f.readline().strip()
        if line == '':
            break
        info = line[:line.index(':')]
        line = line[line.index(':') + 1:].strip()
        if 'time' in info:
            line = datetime.strptime(line, '%m/%d/%Y %H:%M:%S')
            times.append(line)
        elif 'loginid' in info:
            password = f.readline()
            password = password[password.index(':') + 1:].strip()
            logins.append((line, password))
        elif 'link' in info:
            logins.append(line)

time = datetime.now()

closest = None
for c in range(len(times)):
    t = times[c] - datetime.now()
    if closest is None or times[closest] - datetime.now() > t:
        closest = c
print('next class at:\u001b[33m', times[closest])



print('\u001b[0mwaiting for:', round((times[closest]-datetime.now()).total_seconds()/3600, 4), 'hr')
wait = (times[closest]-datetime.now()).total_seconds()/100
for i in range(100):
    if wait < 0:
        break
    sleep.sleep(wait)
    print('#', end='')
print('')

if type(logins[closest]) is tuple:
    config.loginID = logins[closest][0]
    config.password = logins[closest][1]
else:
    config.url = logins[closest]
Zoomer.start(config)
times.remove(closest)
logins.remove(closest)
