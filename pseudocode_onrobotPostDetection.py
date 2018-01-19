import numpy as np
import cv2

class fakeArduino():
	def write(char):
		print("Writing " + char + " to fake Arduino.")
		
arduino = fakeArduino()

def checkPostList(postPossibilities, newLocation):
	if newLocation in postPossibilities:
		return True #we've seen this post before
	else:
		return False
def roundToHalf(num):
	return round(2*num)/2
def checkForObstacles():
	#Check for a stopsign, if we see a stop sign, stop
	#Check for a post directly in front of us and of a certain size (about 2 meters away)
	#If we see this post, return true, and therefore call the generatePath script.
def getLocation():
	return x, y
def moveToWaypoint(currrentLoc, desiredLoc, currentTheta):
	global postStatus
	global x
	global y
	#Here, follow the algorith as already written
	print("moving to next waypoint")
	stopSignDetected, postDetected = checkForObstacles() # come up with something new in GRIP to take care of this situation for detecting a post
	if postDetected and postStatus == False:
		postStatus = True #So if we detected a post and there was previously one undetected, say that we detected one right in front of us.
	elif postDetected == False:
		postStatus = False #If we don't detect a post, keep post status false so we can detect one later!
	if stopSignDetected:
		arduino.write('s')

def generatePath(currentLocation, obstacleList, iterationNumber):
	#find which waypoint we're already closest too.  Call that the new starting waypoint.
	#Use iterationNumber to decide which should be the end waypoint in the triple I if we're coming back or what...

def followWaypointList(waypointList):
	global x
	global y
	for waypoint in waypointList:
		x, y = getLocation()
		stopSignDetected, postDetected = moveToWaypoint((x,y),waypoint,currentTheta)
		if postDetected and postStatus == 0: #For this little if statement, we know that we detected a previously undetected post and mapped it to a position.
			PossiblePostLocation = (x+2*cos(thetaVehicle),y+2*sin(thetaVehicle))
			postPossibilities.append(PossiblePostLocation)
			if not checkPostList(postPossibilities,PossiblePostLocation):
				#if we haven't seen this post before, we need to generate a new path
				waypointList.clear()
				tempList = genereatePath(roundToHalf(x),roundToHalf(y),iterNumber)
				waypointList.extend(tempList)
				return False
		else:
			continue
	return True #If we made it through all the waypoints with no obstacles, return True.

if __name__=='__main__':
	waypointList = generatePath((3.5,3),(3.5,13))
	doneYet = False
	postStatus = False
	while not doneYet:
		doneYet = followWaypointList(waypointList)
	arduino.write('s')
	waypointList.clear()
	waypointList = generatePath((2.5,13),(2.5,4.0))
	doneYet = False
	postStatus = False
	while not doneYet:
		doneYet = followWaypointList(waypointList)
	waypointList.clear()
	waypointList = generatePath((4.5,4.0),(4.5,13.0))
	doneYet = False
	postStatus = False
	while not doneYet:
		doneYet = followWaypointList(waypointList)
	waypointList = generatePath((2.5,13.0),(4.5,2))
	waypointList.clear()
	doneYet = False
	postStatus = False
	while not doneYet:
		doneYet = followWaypointList(waypointList)
	print("Finished, all your snow is plowed!")