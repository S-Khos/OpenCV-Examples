import cv2
import sys
import jetson.inference
import jetson.utils
from adafruit_servokit import ServoKit
import time
import math

myKit = ServoKit(channels=16)

panAngle = 90
tiltAngle = 90
myKit.servo[2].angle = 180 - panAngle
myKit.servo[3].angle = 180 - tiltAngle
width = 1280
height = 720
flip = 0
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

class mnSSD():

	def __init__(self, path, threshold):
		self.path = path
		self.threshold = threshold
		self.net = jetson.inference.detectNet(self.path, self.threshold)
	
	def detect(self, img, display=True):
		imgCuda = jetson.utils.cudaFromNumpy(img)
		detections = self.net.Detect(imgCuda, overlay = "OVERLAY_NONE")
		
		objects = []
		cv2.putText(img, f'FPS {int(self.net.GetNetworkFPS())}', (10,30), font, 1, (255,255,255), 2)
		dt=time.time()-timeStamp
		timeStamp=time.time()
		fps=1/dt
		fpsFilt=.9*fpsFilt + .1*fps
		cv2.putText(frame,'FPS ' + str(round(fpsFilt,1)),(10,50),font,1,(255,255,255),1)
		for entity in detections:

			className = self.net.GetClassDesc(entity.ClassID).upper()
			objects.append([className, entity])
			
			if (display):
				top = int(entity.Top)
				left = int(entity.Left)
				bottom = int(entity.Bottom)
				right = int(entity.Right)
				centreY = int ((top + bottom) / 2)
				centreX = int ((left + right) / 2)
				
				cv2.line(img, (left, top), (left + 20, top), (255,255,255), 2)
				cv2.line(img, (left, top), (left, top + 20), (255,255,255), 2)
				cv2.line(img, (right, top), (right - 20, top), (255,255,255), 2)
				cv2.line(img, (right, top), (right, top + 20), (255,255,255), 2)

				cv2.line(img, (left, bottom), (left + 20, bottom), (255,255,255), 2)
				cv2.line(img, (left, bottom), (left, bottom - 20), (255,255,255), 2)
				cv2.line(img, (right, bottom), (right - 20, bottom), (255,255,255), 2)
				cv2.line(img, (right, bottom), (right, bottom - 20), (255,255,255), 2)

				cv2.putText(img, className, (int(((left + right) / 2)-30),top), font, .7, (0,200,255), 2)
				
		
		return objects
		
		
		



def main():

	camSet='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3264, height=2464, 	framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-.2 saturation=1.2 ! appsink'

	cap = cv2.VideoCapture(camSet)
	

	cv2.namedWindow('FEED', flags=cv2.WINDOW_OPENGL)
	model = mnSSD("ssd-mobilenet-v2", threshold=0.4)
	while True:

		sucess, img = cap.read()
		objects = model.detect(img, True)
		
		cv2.imshow("FEED", img)
		cv2.moveWindow('FEED',0,50)
		cv2.resizeWindow('FEED', 1280,720)
		
		if cv2.waitKey(1)==ord('q'):
			break
	
	cam.release()
	cv.destroyAllWindows()
	


if __name__ == "__main__":
	main()
