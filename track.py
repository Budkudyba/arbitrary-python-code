import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import cv2.cv as old
import numpy as np

width = 320
height= 240
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width,height))

log = open("log",'w')
thresh = 200
max_thrsh = 255
sigma=0.66  #default was .33
font = cv.FONT_HERSHEY_SIMPLEX

time.sleep(0.1)
print("Welcome")

TRACK = False

while(True):
    camera.capture(rawCapture, format="bgr")
    image = cv.flip(rawCapture.array,0)
    raw = cv.flip(rawCapture.array,0) #make a copy #try image.copy()
    
    #clear stream for next frame
    rawCapture.truncate(0)


    if not TRACK: #attempt to find circle
        gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        
        mask = np.zeros((height,width,3),np.uint8) #create a blank mask
        dispCir = np.zeros((height,width,3),np.uint8) #create a blank mask
        
        #define lower and upper bounds of Canny within Hough
        v = np.median(gray)
        lower = int(max(0,(1.0-sigma)*v))
        upper = int(min(255,(1.0+sigma)*v))

        #run Hough
        circles = cv.HoughCircles(gray,old.CV_HOUGH_GRADIENT,1,width/8,param1=lower,param2=upper,minRadius=0,maxRadius=0)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            log.write("circles found: "+ str(circles) +"\n")
            print("circle found!")
            for i in circles[0]:
                cv.circle(mask,(i[0],i[1]),i[2],(255,255,255),-5) #mask the circle
                
                cv.circle(dispCir,(i[0],i[1]),i[2],(0,0,255),1) #radius of circles found
                cv.circle(dispCir,(i[0],i[1]),2,(0,0,255),3) #center of circles found
            found = True
        #make a mask over capture keeping only the ball        
        masked = cv.bitwise_and(mask,raw)
        
        #find low and high intensity
        mask_gray = cv.cvtColor(mask,cv.COLOR_BGR2GRAY)
        minb,maxb,minl,maxl = cv.minMaxLoc(gray,mask_gray)
        log.write(minb+" "+maxb+" "+minl+" "+maxl)
        cv.circle(image,minl,2,(255,0,0),1) #center of circles found
        cv.circle(image,maxl,2,(255,255,255),1) #center of circles found
    
            #show findings
        cv.imshow("masked",masked)
        cv.imshow("Snapshot",image)
        cv.waitKey(0)
        cv.destroyAllWindows()














        
    
