import cv2
import jetson.inference
import jetson.utils
from adafruit_servokit import ServoKit

myKit = ServoKit(channels=16)
panAngle = 90
tiltAngle = 90
myKit.servo[2].angle = 180 - panAngle
myKit.servo[3].angle = 180 - tiltAngle
width = 1280
height = 720
flip = 0
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

camSet='nvarguscamerasrc sensor-id=0 ee-mode=1 ee-strength=0 tnr-mode=2 tnr-strength=1 wbmode=3 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1,format=NV12 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(width)+', height='+str(height)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.3 brightness=-.2 saturation=1.2 ! appsink'

cap = cv2.VideoCapture(camSet)

cv2.namedWindow('FEED',  flags=cv.WINDOW_OPENGL)

while True:
	sucess, img = cap.read()
	imgCuda = jetson.utils.cudaFromNumpy(img)
	
	detections = net.Detect(imgCuda)
	
	for detect in detections:
		ID = detect.ClassID
		top = int(detect.Top)
		left = int(detect.Left)
		bottom = int(detect.Bottom)
		right = int(detect.Right)
		centreY = int ((top + bottom) / 2)
		centreX = int ((left + right) / 2)
		item = net.GetClassDesc(ID).upper()
		
		cv2.rectangle(img, (left,top), (right,bottom), (255,255,255), 1)
		cv2.putText(img, item, (int(((left + right) / 2)-30),top), font, .5, (0,200,255), 2)	
	
	cv2.imshow("FEED", img)
	if cv2.waitKey(1)==ord('q'):
		break

cam.release()
cv.destroyAllWindows()
