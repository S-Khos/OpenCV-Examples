import numpy as np
import jetson.inference
import jetson.utils
import argparse
import sys
import time
import math
from adafruit_servokit import ServoKit
import cv2 as cv
myKit = ServoKit(channels=16)

panAngle = 90
tiltAngle = 90
width = 1280
height = 720
x_lock = 0
y_lock = 0
evt = -1
target = ""
lockOn = False
auto = True
font = cv.FONT_HERSHEY_COMPLEX_SMALL

timeStamp = time.time()
fpsFilt = 0

input = jetson.utils.videoSource('csi://0',  ['--flip-method=rotate-180','–input-width=3264', '–input-height=2464'])
#3264x2464


net = jetson.inference.detectNet("ssd-mobilenet-v1", threshold=0.4)

#net = jetson.inference.detectNet(argv=['--model=jetson-inference/python/training/detection/ssd/models/banana/ssd-mobilenet.onnx', '--labels=jetson-inference/python/training/detection/ssd/models/banana/labels.txt', '--input-blob=input_0','--output-cvg=scores', '--output-bbox=boxes'],threshold=0.5)

def click(event, xSelect, ySelect, flags, params):
	global x_lock
	global y_lock
	global evt
	if event == cv.EVENT_LBUTTONDOWN:
		x_lock = xSelect
		y_lock = ySelect
		evt = event
		

 
cv.namedWindow('feed',  flags=cv.WINDOW_OPENGL)
cv.setMouseCallback('feed', click)

while True:
	myKit.servo[2].angle = 180 - panAngle
	myKit.servo[3].angle = 180 - tiltAngle

	
	img = input.Capture()

	detections = net.Detect(img, width, height, overlay='none')
	frame = jetson.utils.cudaToNumpy(img, width, height, 4)

	frame = cv.cvtColor(frame.astype(np.uint8), cv.COLOR_RGBA2BGR)
	
	if (auto):
		cv.rectangle(frame, (129,10),(191,29), (255,255,255), -1)
		cv.putText(frame, "AUTO", (130,25), font, 1, (0,0,0), 1)
	

	for detect in detections:
		ID = detect.ClassID
		top = int(detect.Top)
		left = int(detect.Left)
		bottom = int(detect.Bottom)
		right = int(detect.Right)
		centreY = int ((top + bottom) / 2)
		centreX = int ((left + right) / 2)
		item = net.GetClassDesc(ID).upper()
		

		cv.line(frame, (left, top), (left + 20, top), (255,255,255), 2)
		cv.line(frame, (left, top), (left, top + 20), (255,255,255), 2)
		cv.line(frame, (right, top), (right - 20, top), (255,255,255), 2)
		cv.line(frame, (right, top), (right, top + 20), (255,255,255), 2)

		cv.line(frame, (left, bottom), (left + 20, bottom), (255,255,255), 2)
		cv.line(frame, (left, bottom), (left, bottom - 20), (255,255,255), 2)
		cv.line(frame, (right, bottom), (right - 20, bottom), (255,255,255), 2)
		cv.line(frame, (right, bottom), (right, bottom - 20), (255,255,255), 2)

		cv.putText(frame, item, (int(((left + right) / 2)-30),top), font, .5, (0,200,255), 2)
		
		if (evt == 1):
			if (len(detections) != 0 and x_lock >= detect.Left and x_lock <= detect.Right and y_lock <= detect.Bottom and y_lock >= detect.Top):
				target = item
				evt = -1
				
				
		if (lockOn):
		
			cv.rectangle(frame, (10,630),(70,660), (255,255,255), -1)
			cv.putText(frame, "LOCK", (10,650), font, 1, (0,0,0), 1)
			cv.rectangle(frame, (10,670),(85,700), (255,255,255), -1)
			cv.putText(frame, "CLEAR", (10,690), font, 1, (0,0,0), 1)

			cv.line(frame, (int(width / 2) - 50, int(height / 2)), (int(width / 2) - 10, int(height / 2)), (0,255,0), 2)
			cv.line(frame, (int(width / 2) + 50, int(height / 2)), (int(width / 2) + 10, int(height / 2)), (0,255,0), 2)
			cv.line(frame, (int(width / 2), int(height / 2) - 50), (int(width / 2), int(height / 2) - 10), (0,255,0), 2)
			cv.line(frame, (int(width / 2), int(height / 2) + 50),(int(width / 2), int(height / 2) +  10) , (0,255,0), 2)
			
			blue = frame[centreY,centreX,0]
			green = frame[centreY,centreX,1]
			red = frame[centreY,centreX,2]
			
			colorSize = cv.getTextSize("CLR "+str(red) + " " + str(blue) + " " + str(green),font,1,1)
			#cv.rectangle(frame, (width - colorSize[0][0] - 10,590),(1270,620), (255,255,255), -1)
			cv.putText(frame, "CLR "+ str(red) + " " + str(blue) + " " + str(green), (width - colorSize[0][0] -10,590), font, 1, (255,255,255), 1)
			
			
		if (item == target):
			itemSize = cv.getTextSize("TRG "+item,font,1,1)
			#cv.rectangle(frame, (width - itemSize[0][0] - 10,630),(1270,660), (255,255,255), -1)
			cv.putText(frame, "TRG "+item, (width - itemSize[0][0] -10,620), font, 1, (255,255,255), 1)
			
			if (width/2 <= right and width/2 >= left and height/2 <= bottom and height/2 >= top):			
				lockOn = True
			frame = cv.circle(frame, (centreX, centreY), 5, (0,0,255), -1)
			panError = int((width / 2) - centreX)
			tiltError = int((height / 2) - centreY)
			cv.putText(frame, "P-E "+ str(abs(panError)),(10,590),font,1,(255,255,255),1)
			cv.putText(frame, 'T-E '+str(abs(tiltError)), (10,620), font, 1, (255,255,255), 1)
			
			if (abs(panError) > 8 and int(panAngle - panError / 20) <= 180 and int(panAngle - panError / 20) >= 0):
				panAngle = int(panAngle - panError / 20)
			if (abs(tiltError) > 8 and int(tiltAngle + tiltError / 20) <= 180 and int(tiltAngle + tiltError / 20) >= 0):
				tiltAngle = int(tiltAngle + tiltError / 20)
		else:
			lockOn = False
	
	dt=time.time()-timeStamp
	timeStamp=time.time()
	fps=1/dt
	fpsFilt=.9*fpsFilt + .1*fps
	cv.putText(frame,'FPS ' + str(round(fpsFilt,1)),(10,25),font,1,(255,255,255),1)
	cv.putText(frame, 'P ' + str(panAngle), (10,45), font, 1, (255,255,255), 1)
	cv.putText(frame, 'T ' + str(tiltAngle), (10,65), font, 1, (255,255,255), 1)	
	# arrow
	cv.circle(frame, (int(width/2) + 60,height - 55), 50, (255,255,255), 1)
	cv.circle(frame, (int(width/2) - 60,height - 55), 50, (255,255,255), 1)
	cv.arrowedLine(frame, (int(width/2) + 60, height - 55), (round(-50 * math.cos(math.radians(panAngle)) + (width/2) + 60), round((height-55) - (50 * math.sin(math.radians(panAngle))))), (255,255,255), 1, tipLength = .2)
	cv.line(frame, (int(width/2) + 60, height - 55), (int(width / 2) + 60, height - 105), (255,255,255), 1)
	cv.imshow('feed',frame)
	cv.moveWindow('feed',0,50)
	cv.resizeWindow('feed', 1280,720)

	if cv.waitKey(1)==ord('q'):
		break
	if cv.waitKey(1) == ord('c'):
		evt = -1
		target = ""
		lockOn = False
		tiltAngle = 90
		panAngle = 90
	#if cv.waitKey(1) == ord(2490368):
	#	tiltAngle += 10
	#if cv.waitKey(1) == ord(2621440):
	#	tiltAngle -= 10
	
		

cam.release()
cv.destroyAllWindows()

