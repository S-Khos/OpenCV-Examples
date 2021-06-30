import cv2 as cv
displayWidth = 640
displayHeight = 480
flip = 0

camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv.VideoCapture(camSet)
while True:
    response, frame = cam.read()
    #colored
    cv.imshow('color feed', frame)
    cv.moveWindow('color feed',0,0)
    #gray feed
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow('grayscale feed', gray)
    cv.moveWindow('grayscale feed', 0,480)

    if (cv.waitKey(1) == ord('q')):
        break

cam.release()
cv.destroyAllWindows()