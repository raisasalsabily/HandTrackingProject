import cv2
import time
import numpy as np
import math
import HandTrackingModule as htm

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

# volume configuration
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]


while True:
    # Membaca setiap img (frame) dari webcam
    success, img = cap.read()
    img = detector.findHands(img) 
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8]) # ujung jempol dan telunjuk

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # get the center of the line 
        cx, cy = (x1+x2)//2, (y1+y2)//2


        cv2.circle(img, (x1, y1), 11, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 11, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        # draw center of the line
        cv2.circle(img, (cx,cy), 11, (255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length) 

        # hand range 50 - 300
        # volume range: -45 - 0
        # convert hand range to volume range
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(0, None)

        # change color to green if length < 50
        if length<50:
            cv2.circle(img, (cx,cy), 11, (0,255,0), cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Jika img berhasil dibaca
    if success:
        # Menampilkan img pada jendela "Webcam"
        cv2.imshow("Image", img)

    # Untuk keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break