import cv2
import grip
import numpy as np

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)





cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
pipeline = grip.GripPipeline()
wlist = []
centerList = []
for i in range(0,20):
	wlist.append(0)
	centerList.append(0)
counter = 0
numSamples = 20
while True:
	for i in np.arange(0,numSamples):
		ret, frame = cap.read()
		pipeline.process(frame)
		cnts = pipeline.convex_hulls_output
		
		try:
			firstCnt = max(cnts, key = cv2.contourArea)
			x,y,w,h = cv2.boundingRect(firstCnt)
			try:
				# x = int(rect[0])
				# w = int(rect[2])
				center = x+w/2
				wlist[i] = w
				centerList[i] = center
				avgW = sum(wlist)/float(len(wlist))
				avgCenter = sum(centerList)/float(len(centerList))
				print("center, width: " + str(avgCenter)+", "+str(avgW))
				#print(str(center)+ ' ' + str(w))
			
			except:
				print("slicing tuple wrong")

			drawnRect = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,255),2)
			cv2.imshow('rectangle',drawnRect)
			key = cv2.waitKey(1) & 0xFF
		
		except:
			print("Something is wrong")
			cv2.imshow('frame', frame)
			key = cv2.waitKey(1) & 0xFF
			#print("Fuck")