import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import cv2.cv as old
import numpy as np
from reduceTowardCenter import fromCenter

width = 640
height= 480

camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width,height))

print("Welcome")
log = open("log",'w')

thresh = 200
max_thrsh = 255
sigma=0.66  #default was .33
font = cv.FONT_HERSHEY_SIMPLEX

time.sleep(0.1)

def grab_circle():
    print("searching for circle...")
    found = False
    mask = np.zeros((height,width,3),np.uint8) #create a blank mask
    while(not found):
        camera.capture(rawCapture, format="bgr")
        image = cv.flip(rawCapture.array,0)
        raw = cv.flip(rawCapture.array,0) #make a copy #try image.copy()

        #clear stream for next frame
        rawCapture.truncate(0)
        
        gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        v = np.median(gray)
        center = [0,0]        
        #define lower and upper bounds of Canny within Hough
        lower = int(max(0,(1.0-sigma)*v))
        upper = int(min(255,(1.0+sigma)*v))
        #run Hough
        circles = cv.HoughCircles(gray,old.CV_HOUGH_GRADIENT,1,1000,param1=lower,param2=upper,minRadius=0,maxRadius=0)
        #show circles found
        if circles is not None:
            circles = np.uint16(np.around(circles))
            print("circle found!")
            for i in circles[0]:
                cv.circle(mask,(i[0],i[1]),i[2],(255,255,255),-5) #mask the circle
                
                cv.circle(image,(i[0],i[1]),i[2],(0,0,255),1) #radius of circles found
                cv.circle(image,(i[0],i[1]),2,(0,0,255),3) #center of circles found
                center = [i[0],i[1]]
            #cv.imshow("Snapshot",image)
            #cv.waitKey(0)
            found = True
                
    masked = cv.bitwise_and(mask,raw) #make a mask over capture keeping only the ball

    #find low and high intensity
    mask_gray = cv.cvtColor(mask,cv.COLOR_BGR2GRAY)
    minb,maxb,minl,maxl = cv.minMaxLoc(gray,mask_gray)
    print(minb,maxb,minl,maxl)

    #walk min and max loc toward center (to not grab wrong color on edge)
    minl = fromCenter(minl,center,80)#point,center,percent
    maxl = fromCenter(maxl,center,80)#point,center,percent
    log.write("Color Points: "+str(minb)+" "+str(maxb)+" "+str(minl)+" "+str(maxl)+"\n")

    cv.circle(image,minl,2,(255,0,0),1) #center of circles found
    cv.circle(image,maxl,2,(255,255,255),1) #center of circles found
    
    #grab low and high colors from HSV image
    #bug sometimes minMaxLoc gives a out of bounds location?
    rawHSV = cv.cvtColor(raw, cv.COLOR_BGR2HSV)
    minc = rawHSV[minl]
    maxc = rawHSV[maxl]
    log.write("minColor: " + str(minc) +"\n")
    log.write("maxColor: " + str(maxc) +"\n")
    print(minc,maxc)

    #show findings
    cv.imshow("masked",masked)
    cv.imshow("Snapshot",image)
    cv.waitKey(0)

    return(minc,maxc)
        
search = True
while(search):
    min_color,max_color = grab_circle()
    an = raw_input('is this picture valid? (y:n) :').lower()
    if an == "y":
        search = False
    else:
        cv.destroyAllWindows()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    start_time = time.time()
    image = cv.flip(frame.array,0)

    imgHSV = cv.cvtColor(image, cv.COLOR_BGR2HSV)
     
    #ranged = cv.inRange(imgHSV, (5,255,120),(20,255,150)) #original numbers
    #ranged = cv.inRange(imgHSV, (5,255,96),(20,255,150)) # better
    #ranged = cv.inRange(imgHSV, (5,255,85),(20,255,150)) # better
    
    #(array([  6, 255,  96], dtype=uint8), array([ 14, 255,  28], dtype=uint8))
    #(array([ 41, 219,  84], dtype=uint8), array([ 46, 209, 105], dtype=uint8))
    #(array([34, 47, 76], dtype=uint8), array([106, 100,  28], dtype=uint8))
    ranged = cv.inRange(imgHSV, min_color, max_color)
    
    total_time = time.time()-start_time
    cv.putText(ranged,str(total_time),(10,200), font,1,(255,255,255),2,cv.CV_AA)

    cv.imshow("Ranged",ranged)
    
    #clear stream for next frame
    rawCapture.truncate(0)
    
    key = cv.waitKey(1) & 0xFF
    # q key breaks loop
    if key == ord("q"):
        break
cv.destroyAllWindows()
