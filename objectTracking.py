import cv2 as cv
import jetson.inference
import jetson.utils
import time
import numpy as np
from adafruit_servokit import ServoKit

myKit = ServoKit(channels=16)

panAngle = 90
tiltAngle = 90
myKit.servo[1].angle = panAngle
myKit.servo[0].angle = tiltAngle
 
timeStamp = time.time()
fpsFilt = 0
net = jetson.inference.detectNet('ssd-mobilenet-v2',threshold=.3)

displayWidth = 1280
displayHeight = 720
flip = 0
font = cv.FONT_HERSHEY_SIMPLEX

camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 !  video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(displayWidth)+', height='+str(displayHeight)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 !  appsink'

cam = cv.VideoCapture(camSet)
 
# Gstreamer code for improvded Raspberry Pi Camera Quality
#camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 ! video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 ! appsink'
#cam=cv2.VideoCapture(camSet)
#cam=jetson.utils.gstCamera(dispW,dispH,'0')
 
#cam=jetson.utils.gstCamera(dispW,dispH,'/dev/video1')
#display=jetson.utils.glDisplay()
#while display.IsOpen():
	

while True:
    #img, width, height= cam.CaptureRGBA()
	myKit.servo[1].angle = panAngle
	myKit.servo[0].angle = tiltAngle
	_,img = cam.read()
	height=img.shape[0]
	width=img.shape[1]
	frame=cv.cvtColor(img,cv.COLOR_BGR2RGBA).astype(np.float32)
	frame=jetson.utils.cudaFromNumpy(frame)
	detections=net.Detect(frame, width, height)
    
	frame = cv.line(img, (0, int(height / 2)), (int(width / 2), int(height / 2)), (0,255,0), 1)
	frame = cv.line(img, (width, int(height / 2)), (int(width / 2), int(height / 2)), (0,255,0), 1)
	frame = cv.line(img, (int(width / 2), 0), (int(width / 2), int(height / 2)), (0,255,0), 1)
	frame = cv.line(img, (int(width / 2), height),(int(width / 2), int(height / 2)), (0,255,0), 1)
	for detect in detections:
		ID=detect.ClassID
		top=int(detect.Top)
		left=int(detect.Left)
		bottom=int(detect.Bottom)
		right=int(detect.Right)
		centreY = int ((top + bottom) / 2)
		centreX = int ((left + right) / 2)
		item=net.GetClassDesc(ID)
		frame = cv.rectangle(img, (left,top),(right,bottom), (0,255,0), 2)
		#frame = cv.line(img, (left, top), (left, int(top + bottom / 2) - 20), (255,255,255), 2)
		#frame = cv.line(img, (left, bottom), (left, int(top + bottom / 2) + 20), (255,255,255), 2)
		#frame = cv.line(img, (right, top), (right, int(top + bottom / 2) - 20), (255,255,255), 2)
		#frame = cv.line(img, (right, bottom), (right, int(top + bottom / 2) + 20), (255,255,255), 2)

		#frame = cv.line(img, (right, top), (int(right - left / 2) + 20, top), (255,255,255), 2)
		#frame = cv.line(img, (left, top), (int(right - left / 2) - 20, top), (255,255,255), 2)
		#frame = cv.line(img, (right, bottom), (int(right- left / 2) + 20, bottom), (255,255,255), 2)
		#frame = cv.line(img, (left, bottom), (int(right - left / 2) - 20, bottom), (255,255,255), 2)

		frame = cv.putText(img, item, (left,top),font,1, (0,255,0,255), 1) 
		frame = cv.circle(img, (int(displayWidth / 2),int(displayHeight / 2)), 10, (0,255,0), -1)
		frame = cv.putText(img, 'Pan: '+str(panAngle), (0,100), font, 1, (255,255,255), 1)
		frame = cv.putText(img, 'Tilt: '+str(tiltAngle), (0,150), font, 1, (255,255,255), 1) 
		if (item == "person"):
			panError = int((width / 2) - centreX)
			tiltError = int((height / 2) - centreY)
			frame = cv.putText(img, 'Pan Error: '+str(abs(panError)), (0,200), font, 1, (0,0,255), 1) 
			frame = cv.putText(img, 'tilt Error: '+str(abs(tiltError)), (0,250), font, 1, (0,0,255), 1)
			#if (abs(panError) > 15 and (panAngle - panError / 130) <= 160  and (panAngle - panError / 130) >= 2):
			#	panAngle = int(panAngle - panError / 130)
			#if (abs(tiltError) > 15 and (tiltAngle - tiltError / 130) <= 160 and (tiltAngle - tiltError / 130) >= 2):
			#	tiltAngle = int(tiltAngle + tiltError / 130)
			if (abs(panError) > 5):
				panAngle = int(panAngle - panError / 140)
			if (abs(tiltError) > 5):
				tiltAngle = int(tiltAngle + tiltError / 140)
	
			frame = cv.circle(img, (int(centreX),int(centreY)), 5, (0,0,255), -1)
            
            


    #display.RenderOnce(img,width,height)
	dt=time.time()-timeStamp
	timeStamp=time.time()
	fps=1/dt
	fpsFilt=.9*fpsFilt + .1*fps
	#cv.putText(img,str(round(fpsFilt,1))+' fps',(0,30),font,1,(0,0,255),2)
	cv.imshow('detCam',img)
	cv.moveWindow('detCam',0,0)
	if cv.waitKey(1)==ord('q'):
		break
	if cv.waitKey(1) == ord('c'):
		panAngle = 90
		tiltAngle = 90

cam.release()
cv.destroyAllWindows()
