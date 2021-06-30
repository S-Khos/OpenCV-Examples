import cv2 as cv

displayWidth = 740
displayHeight = 580
flip = 0

camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv.VideoCapture(camSet)

while True:
    response, frame = cam.read()
    roi = frame[int(displayWidth/2):740, int(displayHeight/2):580]
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
    cv.imshow('roi', gray)

    cv.imshow('feed', frame)
    cv.moveWindow('feed', 0 ,0)
    cv.moveWindow('roi', displayWidth+10,0)

    if (cv.waitKey(1) == ord('q')):
        break

cam.release()
cv.destroyAllWindows()