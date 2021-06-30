from os import X_OK
import cv2 as cv
from adafruit_servokit import ServoKit

myKit = ServoKit(channels=16)

angle = 90

displayWidth = 640
displayHeight = 480
flip = 0
evt = -1
circleCoords = []

def click(event, xSelect, ySelect, flags, params):
    global x 
    global y
    global evt
    if event == cv.EVENT_LBUTTONDOWN:
        x = xSelect
        y = ySelect
        evt = event
        circleCoords.append((x,y))
    if event == cv.EVENT_RBUTTONDOWN:
        x = xSelect
        y = ySelect
        blue = frame[y,x,0]
        green = frame[y,x,1]
        red = frame[y,x,2]
        print(blue, ',',green,',',red)
        
cv.namedWindow('feed')
cv.setMouseCallback('feed', click)

camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv.VideoCapture(camSet)


while True:
    response, frame = cam.read()
    fnt = cv.FONT_HERSHEY_PLAIN
    myKit.servo[0].angle = angle;

    if evt == 1:
        for coord in circleCoords:

            cv.circle(frame,coord, 5, (0,0,255), -1)        
            point = str(coord)
            cv.putText(frame, point, coord, fnt, 1, (0,255,0),2)



    cv.imshow('feed', frame)
    cv.moveWindow('feed', 0 , 0)



    keyEvent = cv.waitKey(1)
    if (keyEvent == ord('q')):
        break
    if (keyEvent == ord('c')):
        circleCoords = []
    if (keyEvent == ord(';')):
        angle += 5
    if (keyEvent == ord('[')):
        angle -= 5
        

cam.release()
cv.destroyAllWindows()