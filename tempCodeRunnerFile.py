import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=1)
colorR = (255,0,255)

cx, cy, w, h = 100,100,200,200

class DragRect():
    def __init__(self, posCenter, size=[200,200]):
        self.posCenter = posCenter
        self.size = size

    def update(self,cursor):
        cx,cy = self.posCenter
        w, h = self.size

        # jika ujung jari jempol di dalam area persegi panjang
        if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2:
            # colorR = 0,255,0
            self.posCenter = cursor # simple drag

rectList = []
# range(jumlah persegi)
for x in range(4):
    rectList.append(DragRect([x*250+150, 150]))

while True:
    # Membaca setiap img (frame) dari webcam
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList:

        """ note: 8, 12: telunjuk, jari tengah
            4,8: jempol, telunjuk """

        l, _, _ = detector.findDistance(4, 8, img, draw=False)
        print(l)
        if l < 30:
            # note: lmList[jari awal]
            cursor = lmList[4]

            # panggil fungsi update di sini
            for rect in rectList:
                rect.update(cursor)

    ## Draw solid
    # for rect in rectList:
    #     cx, cy = rect.posCenter
    #     w, h = rect.size

    #             # jika jari di dalam bangun:
                
    #             # # jika jari tidak di dalam bangun:
    #             # else: 
    #             #     colorR = (255,0,255)

    #     cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED)
    #     cvzone.cornerRect(img, (cx-w//2,cy-h//2, w, h), 20, rt=0)


    ## Draw dengan transparansi
    imgNew = np.zeros_like(img, np.uint8)

    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED)
        cvzone.cornerRect(img, (cx-w//2,cy-h//2, w, h), 20, rt=0)

    out = img.copy()
    alpha = 0.1
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1-alpha, 0)[mask]




    # Jika img berhasil dibaca
    if success:
        # Menampilkan img pada jendela "Webcam"
        cv2.imshow("Image", img)

    # Untuk keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break