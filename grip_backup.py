import cv2
import grip
import numpy as np
from time import sleep
from math import pow
from math import sin
from math import cos
from math import tan
pi = 3.14159
thetaT = -158*pi/180

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
	
def roundToHalf(num):
	return round(num*2)/2
	
def scaleWidth(w, c):
	dfc = abs(640-c)
	ratio = 8*pow(10,-7)*dfc*dfc+8*pow(10,-5)*dfc+.9958
	newWidth = w/ratio
	return newWidth
	
def transX(x, y):
	newX = x*cos(thetaT)-y*sin(thetaT)-7
	return -newX

def transY(x,y):
	newY = x*sin(thetaT)+y*cos(thetaT)+0
	return -newY


cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
pipeline = grip.GripPipeline()
wlist = []
centerList = []
counter = 0
numSamples = 100
for i in range(0,numSamples):
	wlist.append(0)
	centerList.append(0)
while True:
	for i in np.arange(0,numSamples):
		ret, frame = cap.read()
		pipeline.process(frame)
		#print("Frame processed")
		cnts = pipeline.convex_hulls_output
		try:
			firstCnt = max(cnts, key = cv2.contourArea)
			rect = cv2.minAreaRect(firstCnt)
			try:
				x = int(rect[0][0])
				y = int(rect[0][1])
				w = int(rect[1][0])
				h = int(rect[1][1])
				if(w>h):
					temp = w
					w = h
					h = temp
				#bottom left: x, y+h, bottom right: x+w, y+has_key
				center = x+w/2
				#w = scaleWidth(w,center)
				wlist[i] = w
				centerList[i] = center
				avgW = sum(wlist)/float(len(wlist))
				avgCenter = sum(centerList)/float(len(wlist))
				dist = 81.297*pow(avgW,-0.874)
				coneTheta = translate(avgCenter, 0, 1280, -37, 37)
				#print("center, width, dist, coneTheta: " + str(avgCenter)+", "+str(avgW)+", "+str(dist)+", "+str(coneTheta))
				yPost = roundToHalf(dist*cos(coneTheta*pi/180))
				xPost = roundToHalf(dist*sin(coneTheta*pi/180))
				xTrans = transX(xPost,yPost)
				yTrans = transY(xPost,yPost)
				print("(x,y): ("+str(xPost)+","+str(yPost)+")")
				#print("(x,y), theta: ("+str(xTrans)+","+str(yTrans)+"), "+str(thetaT*180/pi))
			
			except:
				print("slicing tuple wrong")
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			drawnRect = cv2.drawContours(frame,[box],0,(255,0,255),2)
			cv2.imshow('rectangle',drawnRect)
			key = cv2.waitKey(1) & 0xFF
			if key==ord("u"):
				thetaT+=pi/180
			if key==ord("d"):
				thetaT-=pi/180
		except:
			# cv2.imshow('frame', frame)
			# key = cv2.waitKey(1) & 0xFF
			print("Fuck")