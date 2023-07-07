import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0 
cTime = 0 # current time
# Membuka webcam
cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    # Membaca setiap img (frame) dari webcam
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Jika img berhasil dibaca
    if success:
        # Menampilkan img pada jendela "Webcam"
        cv2.imshow("Image", img)

    # Untuk keluar dari loop jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


