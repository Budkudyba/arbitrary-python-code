import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import cv2.cv as old
import numpy as np

width = 640
height = 480

camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width,height))

print("Welcome")

thresh = 200
max_thrsh = 255
sigma=0.66  #default was .33
font = cv.FONT_HERSHEY_SIMPLEX

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start_time = time.time()
    image = cv.flip(frame.array,0)
    #clear stream for next frame
    rawCapture.truncate(0)

    imgHSV = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    blur = cv.GaussianBlur(imgHSV,(3,3),0)

    #grab only the range(color) we're looking for 
    ranged = cv.inRange(blur, (5,255,85),(20,255,150)) # better


    #filter results to clean out noise
    kernel = np.ones((5,5),np.uint8) #5x5 kernal for erosion/dilate
    opening = cv.morphologyEx(ranged,cv.MORPH_OPEN,kernel)#erode and dilate in one pass

    #find contours to find center of color
    #default to center if not found
    disp = np.zeros((height,width,3),np.uint8)
    cx = width/2
    cy = height/2
    max_area = 0
    
    contours,hierarchy = cv.findContours(opening,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    i = 0
    for cnt in contours:
        moments = cv.moments(cnt)
        if moments['m00']!=0:
            cx_temp = int(moments['m10']/moments['m00']) #cx = M10/M00
            cy_temp = int(moments['m01']/moments['m00']) #cy = M01/M00
            moment_area = moments['m00']    #Contour area from moment
            contour_area = cv.contourArea(cnt)
            if contour_area > max_area: #only take the contour if it's area is larger
                max_area = contour_area
                cx = cx_temp
                cy = cy_temp
            i+=1
        cv.drawContours(disp,[cnt],0,(0,255,0),1) #draw contours in green 
    cv.circle(disp,(cx,cy),50,(0,0,255),2)
    cv.putText(disp,str(i),(10,height-20), font,1,(255,255,0),2,cv.CV_AA) #display number of contours found
    cv.putText(disp,str(max_area),(10,200), font,1,(255,0,0),2,cv.CV_AA) #display max_area
    

    total_time = time.time()-start_time
    cv.putText(disp,str(total_time)[0:5],(10,10), font,1,(255,255,255),2,cv.CV_AA)

    #cv.imshow("Ranged",ranged)
    #cv.imshow("filtered",opening)
    cv.imshow("Contours",disp)
    
    key = cv.waitKey(1) & 0xFF
    # q key breaks loop
    if key == ord("q"):
        break
cv.destroyAllWindows()
