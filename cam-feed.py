import cv2 as cv
displayWidth = 1280
displayHeight = 860
flip = 0

camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv.VideoCapture(camSet)
while True:
    response, frame = cam.read()
    # start from here 
    cv.imshow('camera feed', frame)
    if (cv.waitKey(1) == ord('q')):
        break

cam.release()
cv.destroyAllWindows()