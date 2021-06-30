import cv2 as cv

displayWidth = 640
displayHeight = 480
flip = 0

camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv.VideoCapture(camSet)

dispW = int(cam.get(cv.CAP_PROP_FRAME_WIDTH))
dispH = int(cam.get(cv.CAP_PROP_FRAME_HEIGHT))
BW = int(.15*dispW)
BH = int(.15*dispH)

posX = 10
posY = 170
dx = 4
dy = 4

while True:
    response, frame = cam.read()
    #drawing starts here
    frame = cv.rectangle(frame, (posX,posY),(posX + BW, posY + BH), (255,0,0), -1) #(top left verticie x,y) (bot right verticie x, y), color, line width)
    cv.imshow('feed', frame)
    posX = posX + dx
    posY = posY + dy

    endx = posX + BW
    endy = posY + BH

    if (endx > dispW):
        dx = dx * -1
    if (endy > dispH):
        dy = dy * -1
    if (endx < 0):
        dx = dx * -1
    if (endy < 100):
        dy = dy * -1
    

    cv.moveWindow('feed', 0 ,0)
    if (cv.waitKey(1) == ord('q')):
        break

cam.release()
cv.destroyAllWindows()