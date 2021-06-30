import cv2 as cv

displayWidth = 640
displayHeight = 480
flip = 0

camSet = 'nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv.VideoCapture(camSet)
while True:
    response, frame = cam.read()
    #drawing starts here
    frame = cv.rectangle(frame, (140,100),(180,200), (255,0,0), 1) #(top left verticie x,y) (bot right verticie x, y), color, line width)
    frame = cv.circle(frame, (320, 240), 100, (0,0,255), 1) # centre, radius, color, line width
    fnt = cv.FONT_HERSHEY_DUPLEX #font 
    frame = cv.putText(frame, 'Circle', (280, 140), fnt, 1, (255,0,0), 1) # text, center, font, size, color, thickness
    frame = cv.line(frame, (0, 0), (310, 230), (0,0,255), 2)
    frame = cv.line(frame, (640, 480), (330, 250), (0,0,255), 2)
    frame = cv.arrowedLine(frame, (50,10), (50,100), (0,255,255),1)



    cv.imshow('feed', frame)
    cv.moveWindow('feed', 0 ,0)


    if (cv.waitKey(1) == ord('q')):
        break

cam.release()
cv.destroyAllWindows()