#HueTrack v2.0
#Written by Justin and William

#Imports
import cv2
import numpy as np
import time

#User info
def userInfo(infoBox, img, name, x, y, w):
    font = cv2.FONT_HERSHEY_SIMPLEX

    focal = 858
    pixelW = w
    actualW = 5.5
    distance = (focal * actualW) / pixelW
    
    centerX = 880
    centerY = 360
    currentX = x
    currentY = y
    distanceX = centerX - currentX
    distanceY = centerY - currentY
    cv2.putText(infoBox, "Dashboard", (10, 30), font, .7, (0, 0, 0))
    cv2.putText(infoBox, "Press and hold 'Q' to exit", (900, 50), font, .5, (0, 255, 255))
    cv2.putText(infoBox, "Press and hold 'S' to take a screenshot", (900, 70), font, .5, (0, 255, 255))
    cv2.putText(infoBox, "Distance from center (X) is: " + str(distanceX), (10, 180), font, .5, (0, 150, 255))
    cv2.putText(infoBox, "Distance from center (Y) is: " + str(distanceY), (10, 200), font, .5, (0, 150, 255))
    cv2.putText(infoBox, "Distance from camera is: " + str(distance) + " inches", (10, 220), font, .5, (0, 150, 255))
    
    if (distanceX < 50 and distanceX > -50) and (distanceY < 50 and distanceY > -50):
        cv2.putText(img, "Way to go, " + str(name) + "!", (100, 600), font, 1, (0, 150, 255))    
    else:
        cv2.putText(img, "Hello, " + str(name) + "!" + " Please move the sign to the center of the window.", (100, 700), font, 1, (0, 150, 255))
    return name

#Text to always be displayed
def alwaysText():
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, "Press and hold 'Q' to exit", (900, 50), font, .5, (0, 255, 255))
    cv2.putText(img, "Press and hold 'S' to take a screenshot", (900, 70), font, .5, (0, 255, 255)) 
    cv2.putText(img, "Uh oh! Sign could not be located!", (400, 360), font, 1, (0, 0, 255)) 
    
#Color location and location printing
def colorLocate(x, y, z, w, o, p, color, angle, (b, g, r)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    leftp = "("
    rightp = ")"
    comma = ", "
    
    cv2.putText(infoBox, ("The location of " + color + " is: " + leftp + str(x) + comma + str(y) + rightp), (z, w), font, 0.5, (b, g, r))
    cv2.putText(infoBox, ("The rotation of " + color + " is: " + leftp + str(angle) + rightp), (o, p), font, 0.5, (b, g, r))
    
#Draw rectangles around contours 
#[Initial function, includes call to userInfo]
def drawSquaresInit(infoBox, img, contours, color, z, q, o, p, (b, g, r), lineColor): 
    maxArea = 0
    bestContour = None        
    for contour in contours:
        Area = cv2.contourArea(contour)
        if Area > maxArea:
            bestContour = contour
            maxArea = Area
    if bestContour != None:
        (x,y,w,h) = cv2.boundingRect(bestContour)
        rect = cv2.minAreaRect(bestContour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        img = cv2.drawContours(img,[box],0,lineColor,2) 
        """goodFeats = cv2.goodFeaturesToTrack(grayImg, 5, 0.1, 100)
        for feat in goodFeats:
            cv2.circle(img, (feat[0, 0], feat[0, 1]), (3),
                         (255, 0, 0))   """     
    
        circle = cv2.circle(img, ((x + w/2),(y+ h/2)), 15, lineColor)
        bestContours.append(bestContour)
        
        locX = x + w/2
        locY = y + h/2
    
        userInfo(infoBox, img, name, locX, locY, w)
        colorLocate(locX, locY, z, q, o, p, color, rect[2],(b, g, r))   
  
#Draw rectangles around contours 
def drawSquares(infoBox, img, contours, color, z, q, o, p, (b, g, r), lineColor): 
    maxArea = 0
    bestContour = None        
    for contour in contours:
        Area = cv2.contourArea(contour)
        if Area > maxArea:
            bestContour = contour
            maxArea = Area
    if bestContour != None:
        (x,y,w,h) = cv2.boundingRect(bestContour)
        rect = cv2.minAreaRect(bestContour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        img = cv2.drawContours(img,[box],0, lineColor,2) 
        """goodFeats = cv2.goodFeaturesToTrack(grayImg, 5, 0.1, 100)
        for feat in goodFeats:
            cv2.circle(img, (feat[0, 0], feat[0, 1]), (3),
                         (255, 0, 0))   """     
    
        circle = cv2.circle(img, ((x + w / 2),(y + h / 2)), 15, lineColor)
        bestContours.append(bestContour)
        
        locX = x + w/2
        locY = y + h/2
    
        colorLocate(locX, locY, z, q, o, p, color, rect[2],(b, g, r)) 
           
           
#User input
name = raw_input("Please type your name: ")

#Flash screen
flashImg = cv2.imread("flash.jpg")
flash = cv2.imshow("HueTrack v2.0", flashImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

infoBox = np.ones((275, 420, 3), np.uint8)

camera = cv2.VideoCapture(0)
ret, img = camera.read()   
running = True
while running:
    infoBox[:,:,:] = 255
    #Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    (h, s, v) = cv2.split(hsv)
    
    #Color Ranges
    cNames = ["blue", "purple", "green"]
    ranges = [[np.array([90, 110, 110]), np.array([120, 255, 255])],
              [np.array([120,  80,  80]), np.array([145, 255, 255])],
              [np.array([ 82,  50,  50]), np.array([ 95, 255, 255])]]     
    
    #Color Masks
    masks = [None] * 3
    for i in range (0, 3):
        masks[i] = cv2.inRange (hsv, ranges[i][0], ranges[i][1])

    #Find Contours
    finalImages = [None] * 3
    contoursList = [None] * 3
    hierarchies = [None] * 3
    for i in range (0, len(masks)):
        (finalImages[i], contoursList[i], hierarchies[i]) = cv2.findContours (masks[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
    #Image Processing
    merge = cv2.addWeighted(finalImages[0], 0.5, finalImages[1], 0.5, 0)
    mask = cv2.addWeighted(merge, 1, finalImages[2], 0.5, 0)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    mask = cv2.erode(mask, element, iterations = 3)
    mask = cv2.dilate(mask, element, iterations = 3)
    mask =cv2.erode(mask, element)
    res, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_TOZERO)
    
    bestContours = [None] * 3
    centers = [None] * 3
    for i in range (0, len(contoursList)):
        maxArea = 0
        for contour in contoursList[i]:
            Area = cv2.contourArea(contour)
            if Area > maxArea:
                bestContours[i] = cv2.boundingRect (contour)
                (x, y, w, h) = bestContours[i]
                centers[i] = [x + (w / 2), y + (h / 2)]
                maxArea = Area
    
    if bestContours[2] == None or bestContours[1] == None or bestContours[0] == None:
        continue
    if centers[2] == None or centers[1] == None or centers[0] == None:
        continue


    xMid = (centers[0][0] + centers[2][0])/2.0
    yMid = (centers[0][1] + centers[2][1])/2.0
    
    lineColor = (0, 0, 255)
    
    if abs(xMid - centers[1][0])/xMid < 0.1 and abs(yMid - centers[1][1])/yMid < 0.1:
        lineColor = (0, 255, 0)   
    
    if lineColor == (0, 255, 0):
        drawSquares(infoBox, img, contoursList[0], cNames[0], 10, 60, 10, 120, (255, 0, 0), lineColor)
        drawSquares(infoBox, img, contoursList[1], cNames[1], 10, 80, 10, 140, (230, 0, 80), lineColor)
        drawSquaresInit(infoBox, img, contoursList[2], cNames[2], 10, 100, 10, 160, (0, 235, 0), lineColor)
    else:
        alwaysText()
        
    cv2.imshow("HueTrack v2.0",img)
    cv2.imshow("Dashboard", infoBox)
    #Debugging 
    #cv2.imshow("Mask", mask)
    #cv2.imshow("Mask 1", mask1)
    #cv2.imshow("FinalImg1", finalImg1)
    
    y = cv2.waitKey(10)
    if y > -1 and chr(y) == 's':
        cv2.imwrite("screencap.jpg", img)
    if y > -1 and chr(y) =='q':
        break

cv2.destroyAllWindows()